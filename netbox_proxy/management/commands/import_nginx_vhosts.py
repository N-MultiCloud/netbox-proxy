"""
Management command: import_nginx_vhosts

Parses an nginx config file and idempotently creates ProxySSLCertificate,
ProxyUpstream, ProxyUpstreamServer, ProxyVHost, and ProxyLocation objects
for every HTTPS server block found in the file.

HTTP-only redirect blocks (port 80, return 301) and non-HTTP stream/geo
blocks are skipped.

Usage:
    manage.py import_nginx_vhosts --cluster 1 --config /etc/nginx/nginx-nms.conf
    manage.py import_nginx_vhosts --cluster 1 --config ... --dry-run
"""

import re
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from netbox_proxy.models import (
    ProxyCluster,
    ProxyLocation,
    ProxySSLCertificate,
    ProxyUpstream,
    ProxyUpstreamServer,
    ProxyVHost,
)


# ---------------------------------------------------------------------------
# Minimal nginx block parser
# ---------------------------------------------------------------------------


def _strip_comments(text):
    """Remove # comments (not inside strings)."""
    return re.sub(r"#[^\n]*", "", text)


def _tokenize(text):
    """Yield (type, value) tokens: BLOCK_OPEN, BLOCK_CLOSE, DIRECTIVE."""
    text = _strip_comments(text)
    buf = ""
    for ch in text:
        if ch == "{":
            name = buf.strip()
            buf = ""
            yield ("BLOCK_OPEN", name)
        elif ch == "}":
            if buf.strip():
                yield ("DIRECTIVE", buf.strip())
            buf = ""
            yield ("BLOCK_CLOSE", "")
        elif ch == ";":
            d = buf.strip()
            if d:
                yield ("DIRECTIVE", d)
            buf = ""
        else:
            buf += ch


class _Block:
    __slots__ = ("name", "directives", "children")

    def __init__(self, name):
        self.name = name
        self.directives = []  # list of directive strings (no trailing ;)
        self.children = []  # list of _Block

    def get(self, key, default=None):
        """Return first directive value matching key."""
        for d in self.directives:
            parts = d.split(None, 1)
            if parts and parts[0] == key:
                return parts[1] if len(parts) > 1 else ""
        return default

    def get_all(self, key):
        """Return all values for a directive key."""
        results = []
        for d in self.directives:
            parts = d.split(None, 1)
            if parts and parts[0] == key:
                results.append(parts[1] if len(parts) > 1 else "")
        return results


def _parse_blocks(tokens, parent=None):
    """Recursively parse token stream into _Block tree."""
    while True:
        try:
            ttype, tval = next(tokens)
        except StopIteration:
            break
        if ttype == "BLOCK_OPEN":
            child = _Block(tval)
            if parent is not None:
                parent.children.append(child)
            _parse_blocks(tokens, child)
        elif ttype == "BLOCK_CLOSE":
            return
        elif ttype == "DIRECTIVE":
            if parent is not None:
                parent.directives.append(tval)


def parse_nginx(path):
    """Return the root pseudo-block containing all top-level blocks."""
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    tokens = iter(_tokenize(text))
    root = _Block("root")
    _parse_blocks(tokens, root)
    return root


# ---------------------------------------------------------------------------
# Extraction helpers
# ---------------------------------------------------------------------------

_PROXY_HEADERS = {
    "Host": "$host",
    "Upgrade": "$http_upgrade",
    "X-Real-IP": "$remote_addr",
    "Connection": '"upgrade"',
    "X-Forwarded-For": "$proxy_add_x_forwarded_for",
    "X-Forwarded-Host": "$host",
    "X-Forwarded-Proto": "$scheme",
}


def _listen_parts(block):
    """Return (address, port, ssl) from the first listen directive."""
    for d in block.get_all("listen"):
        parts = d.split()
        ssl = "ssl" in parts
        addr_port = parts[0]
        if ":" in addr_port:
            addr, port = addr_port.rsplit(":", 1)
        else:
            addr, port = "", addr_port
        try:
            port = int(port)
        except ValueError:
            continue
        return addr, port, ssl
    return "", 0, False


def _location_proxy_pass(loc_block):
    """Return the proxy_pass URL from a location block, or ''."""
    return loc_block.get("proxy_pass", "")


def _upstream_name_from_proxy_pass(proxy_pass_url):
    """Convert http://127.0.0.1:3001 → upstream_127_0_0_1_3001."""
    url = re.sub(r"^https?://", "", proxy_pass_url.strip())
    url = url.rstrip("/")
    return "upstream_" + re.sub(r"[^a-zA-Z0-9]", "_", url)


def _server_slug(server_name):
    """Convert nms.nmulti.cloud → nms-nmulti-cloud."""
    return re.sub(r"[^a-zA-Z0-9-]", "-", server_name).strip("-")


# ---------------------------------------------------------------------------
# Main command
# ---------------------------------------------------------------------------


class Command(BaseCommand):
    help = "Import HTTPS server blocks from an nginx config into netbox-proxy"

    def add_arguments(self, parser):
        parser.add_argument(
            "--cluster", required=True, type=int, help="ProxyCluster ID"
        )
        parser.add_argument("--config", required=True, help="Path to nginx config file")
        parser.add_argument(
            "--dry-run", action="store_true", help="Print plan without writing"
        )

    def handle(self, *args, **options):
        dry = options["dry_run"]
        prefix = "[DRY-RUN] " if dry else ""

        try:
            cluster = ProxyCluster.objects.get(pk=options["cluster"])
        except ProxyCluster.DoesNotExist:
            raise CommandError(f"ProxyCluster id={options['cluster']} not found")

        config_path = options["config"]
        if not Path(config_path).exists():
            raise CommandError(f"Config file not found: {config_path}")

        self.stdout.write(f"{prefix}Parsing {config_path} for cluster '{cluster.name}'")
        root = parse_nginx(config_path)

        # Find the http {} block
        http_block = next((b for b in root.children if b.name == "http"), None)
        if http_block is None:
            raise CommandError("No http {} block found in config")

        # Collect HTTPS server blocks (listen *:443 ssl)
        https_servers = []
        for block in http_block.children:
            if block.name.startswith("server"):
                addr, port, ssl = _listen_parts(block)
                if port == 443 and ssl:
                    https_servers.append((addr, block))

        self.stdout.write(f"{prefix}Found {len(https_servers)} HTTPS server blocks")
        if not https_servers:
            self.stdout.write(
                self.style.WARNING("No HTTPS server blocks found. Nothing to import.")
            )
            return

        # --- SSL Certificate ---
        ssl_cert = None
        for _, sb in https_servers:
            cert_path = sb.get("ssl_certificate", "")
            key_path = sb.get("ssl_certificate_key", "")
            if cert_path and key_path:
                ssl_cert_name = "nms-nmulti-cloud-san"
                if not dry:
                    ssl_cert, created = ProxySSLCertificate.objects.get_or_create(
                        name=ssl_cert_name,
                        defaults={
                            "cert_path": cert_path,
                            "key_path": key_path,
                            "description": "Let's Encrypt SAN cert for *.nmulti.cloud",
                        },
                    )
                    action = "created" if created else "exists"
                    self.stdout.write(f"  SSL cert '{ssl_cert_name}' [{action}]")
                else:
                    self.stdout.write(
                        f"  {prefix}Would create SSL cert '{ssl_cert_name}' "
                        f"({cert_path})"
                    )
                break

        # --- Per-server processing ---
        upstream_cache = {}  # proxy_pass_url -> ProxyUpstream instance (or name in dry-run)

        for listen_addr, sb in https_servers:
            server_name = sb.get("server_name", "").split()[0]
            if not server_name:
                continue

            slug = _server_slug(server_name)
            vhost_name = slug

            # Collect custom directives: http2, allowlist check
            custom_parts = []
            if sb.get("http2"):
                custom_parts.append("http2 on;")
            # Add allowlist guard (present in all blocks)
            custom_parts.append("if ($nms_allowed = 0) { return 403; }")
            if sb.get("client_max_body_size"):
                custom_parts.append(
                    f"client_max_body_size {sb.get('client_max_body_size')};"
                )
            custom_directives = "\n".join(custom_parts)

            self.stdout.write(f"\n{prefix}VHost: {server_name} ({listen_addr}:443)")

            if not dry:
                vhost, vcreated = ProxyVHost.objects.get_or_create(
                    cluster=cluster,
                    name=vhost_name,
                    defaults={
                        "server_names": server_name,
                        "listen_port": 0,
                        "listen_ssl_port": 443,
                        "ssl_mode": "cert" if ssl_cert else "off",
                        "ssl_certificate": ssl_cert,
                        "is_enabled": True,
                        "custom_directives": custom_directives,
                        "description": f"Imported from nginx-nms.conf — {server_name}",
                    },
                )
                if vcreated and listen_addr:
                    vhost.custom_field_data["listen_address"] = listen_addr
                    vhost.save(update_fields=["custom_field_data"])
                action = "created" if vcreated else "exists"
                self.stdout.write(f"  VHost '{vhost_name}' [{action}]")
            else:
                self.stdout.write(f"  {prefix}Would create VHost '{vhost_name}'")
                vhost = None

            # --- Location blocks ---
            sort_order = 10
            for loc_block in sb.children:
                if not loc_block.name.startswith("location"):
                    continue
                # location name = "location /" → path = "/"
                loc_name_parts = loc_block.name.split(None, 1)
                if len(loc_name_parts) < 2:
                    path = "/"
                    match_type = "prefix"
                else:
                    spec = loc_name_parts[1].strip()
                    if spec.startswith("~"):
                        match_type = "regex"
                        path = spec.lstrip("~ ").strip()
                    elif spec.startswith("="):
                        match_type = "exact"
                        path = spec.lstrip("= ").strip()
                    else:
                        match_type = "prefix"
                        path = spec

                proxy_pass_url = _location_proxy_pass(loc_block)

                # try_files (static location)
                try_files = loc_block.get("try_files")
                if try_files and not proxy_pass_url:
                    self.stdout.write(
                        f"    {prefix}Location {path} → static (try_files)"
                    )
                    # Create location with no upstream
                    if not dry and vhost:
                        loc_custom = []
                        root_dir = loc_block.get("root") or sb.get("root")
                        if root_dir:
                            loc_custom.append(f"root {root_dir};")
                        expires = loc_block.get("expires")
                        if expires:
                            loc_custom.append(f"expires {expires};")
                        add_header = loc_block.get("add_header")
                        if add_header:
                            loc_custom.append(f"add_header {add_header};")
                        loc_custom.append(f"try_files {try_files};")

                        ProxyLocation.objects.get_or_create(
                            vhost=vhost,
                            path=path,
                            defaults={
                                "match_type": match_type,
                                "proxy_pass_url": "",
                                "proxy_set_headers": {},
                                "sort_order": sort_order,
                                "custom_directives": "\n".join(loc_custom),
                                "description": f"Static files — {server_name}{path}",
                            },
                        )
                    sort_order += 10
                    continue

                if not proxy_pass_url:
                    continue

                # Determine upstream (or direct proxy_pass_url for external hosts)
                upstream = None
                upstream_addr = re.sub(
                    r"^https?://", "", proxy_pass_url.strip()
                ).rstrip("/")
                is_local = upstream_addr.startswith("127.") or upstream_addr.startswith(
                    "10.0."
                )

                if is_local:
                    upstream_name = _upstream_name_from_proxy_pass(proxy_pass_url)
                    if upstream_name not in upstream_cache:
                        if not dry:
                            upstream, ucreated = ProxyUpstream.objects.get_or_create(
                                cluster=cluster,
                                name=upstream_name,
                                defaults={
                                    "protocol": "http",
                                    "balance": "round_robin",
                                    "keepalive": 0,
                                    "description": f"Backend {upstream_addr}",
                                },
                            )
                            if ucreated:
                                ProxyUpstreamServer.objects.get_or_create(
                                    upstream=upstream,
                                    address=upstream_addr,
                                    defaults={"weight": 1, "enabled": True},
                                )
                                self.stdout.write(
                                    f"    Upstream '{upstream_name}' → {upstream_addr} [created]"
                                )
                            else:
                                self.stdout.write(
                                    f"    Upstream '{upstream_name}' [exists]"
                                )
                            upstream_cache[upstream_name] = upstream
                        else:
                            self.stdout.write(
                                f"    {prefix}Would create upstream '{upstream_name}' → {upstream_addr}"
                            )
                            upstream_cache[upstream_name] = upstream_name
                    else:
                        upstream = upstream_cache[upstream_name] if not dry else None

                # Collect proxy_set_headers
                headers = dict(_PROXY_HEADERS)  # start with standard set
                rewrite = loc_block.get("rewrite")
                custom_loc_parts = []
                if rewrite:
                    custom_loc_parts.append(f"rewrite {rewrite} break;")
                read_timeout = loc_block.get("proxy_read_timeout")
                if read_timeout:
                    custom_loc_parts.append(f"proxy_read_timeout {read_timeout};")
                buffering = loc_block.get("proxy_buffering")
                if buffering:
                    custom_loc_parts.append(f"proxy_buffering {buffering};")
                request_buffering = loc_block.get("proxy_request_buffering")
                if request_buffering:
                    custom_loc_parts.append(
                        f"proxy_request_buffering {request_buffering};"
                    )

                if not dry and vhost:
                    ProxyLocation.objects.get_or_create(
                        vhost=vhost,
                        path=path,
                        defaults={
                            "match_type": match_type,
                            "upstream": upstream if is_local else None,
                            "proxy_pass_url": proxy_pass_url if not is_local else "",
                            "proxy_set_headers": headers,
                            "sort_order": sort_order,
                            "custom_directives": "\n".join(custom_loc_parts),
                            "description": f"{server_name}{path} → {upstream_addr}",
                        },
                    )
                    self.stdout.write(f"    Location {path} → {upstream_addr}")
                else:
                    self.stdout.write(
                        f"    {prefix}Would create location {path} → {upstream_addr}"
                    )

                sort_order += 10

            # Static alias locations (alias directive, e.g. /static/ in netbox.nmulti.cloud)
            for loc_block in sb.children:
                if not loc_block.name.startswith("location"):
                    continue
                alias = loc_block.get("alias")
                if not alias:
                    continue
                loc_name_parts = loc_block.name.split(None, 1)
                path = loc_name_parts[1].strip() if len(loc_name_parts) > 1 else "/"

                custom_loc_parts = [f"alias {alias};"]
                access_log = loc_block.get("access_log")
                if access_log:
                    custom_loc_parts.append(f"access_log {access_log};")
                expires = loc_block.get("expires")
                if expires:
                    custom_loc_parts.append(f"expires {expires};")

                if not dry and vhost:
                    ProxyLocation.objects.get_or_create(
                        vhost=vhost,
                        path=path,
                        defaults={
                            "match_type": "prefix",
                            "proxy_pass_url": "",
                            "proxy_set_headers": {},
                            "sort_order": sort_order,
                            "custom_directives": "\n".join(custom_loc_parts),
                            "description": f"{server_name}{path} → static alias",
                        },
                    )
                    self.stdout.write(f"    Location {path} → alias {alias}")
                else:
                    self.stdout.write(
                        f"    {prefix}Would create location {path} → alias {alias}"
                    )

                sort_order += 10

        self.stdout.write(self.style.SUCCESS(f"\n{prefix}Import complete."))
