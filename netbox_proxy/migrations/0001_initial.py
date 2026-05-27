from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("contenttypes", "0002_remove_content_type_name"),
        ("netbox_nms", "0001_initial"),
        ("netbox_rpc", "0001_initial"),
    ]

    operations = [
        # ── ProxyCluster ──────────────────────────────────────────────────────
        migrations.CreateModel(
            name="ProxyCluster",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("custom_field_data", models.JSONField(blank=True, default=dict)),
                ("name", models.CharField(max_length=255, unique=True)),
                ("description", models.CharField(blank=True, max_length=500)),
                ("comments", models.TextField(blank=True)),
            ],
            options={
                "verbose_name": "Proxy Cluster",
                "ordering": ("name",),
            },
        ),
        # ── ProxySSLCertificate ───────────────────────────────────────────────
        migrations.CreateModel(
            name="ProxySSLCertificate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("custom_field_data", models.JSONField(blank=True, default=dict)),
                ("name", models.CharField(max_length=255, unique=True)),
                (
                    "provider",
                    models.CharField(
                        choices=[
                            ("manual", "Manual"),
                            ("letsencrypt", "Let's Encrypt"),
                            ("selfsigned", "Self-Signed"),
                        ],
                        default="manual",
                        max_length=20,
                    ),
                ),
                ("domain", models.CharField(max_length=255)),
                ("cert_path", models.CharField(blank=True, max_length=500)),
                ("key_path", models.CharField(blank=True, max_length=500)),
                ("chain_path", models.CharField(blank=True, max_length=500)),
                ("auto_renew", models.BooleanField(default=False)),
                ("expires_at", models.DateTimeField(blank=True, null=True)),
                ("custom_directives", models.TextField(blank=True)),
                ("description", models.CharField(blank=True, max_length=500)),
                ("comments", models.TextField(blank=True)),
            ],
            options={
                "verbose_name": "Proxy SSL Certificate",
                "ordering": ("name",),
            },
        ),
        # ── ProxyRateLimit ────────────────────────────────────────────────────
        migrations.CreateModel(
            name="ProxyRateLimit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("custom_field_data", models.JSONField(blank=True, default=dict)),
                ("name", models.CharField(max_length=255, unique=True)),
                ("zone_name", models.CharField(blank=True, max_length=255)),
                ("key", models.CharField(blank=True, default="$binary_remote_addr", max_length=255)),
                ("rate", models.CharField(max_length=50)),
                ("burst", models.PositiveIntegerField(default=5)),
                ("nodelay", models.BooleanField(default=False)),
                ("description", models.CharField(blank=True, max_length=500)),
                ("comments", models.TextField(blank=True)),
            ],
            options={
                "verbose_name": "Proxy Rate Limit",
                "ordering": ("name",),
            },
        ),
        # ── ProxyNode ─────────────────────────────────────────────────────────
        migrations.CreateModel(
            name="ProxyNode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("custom_field_data", models.JSONField(blank=True, default=dict)),
                ("name", models.CharField(max_length=255)),
                (
                    "assigned_object_id",
                    models.PositiveBigIntegerField(
                        blank=True,
                        null=True,
                        verbose_name="Assigned object ID",
                    ),
                ),
                ("management_ip", models.CharField(blank=True, max_length=255)),
                ("nginx_config_path", models.CharField(blank=True, default="/etc/nginx", max_length=500)),
                ("nginx_binary", models.CharField(blank=True, default="/usr/sbin/nginx", max_length=500)),
                ("is_active", models.BooleanField(default=True)),
                ("last_seen", models.DateTimeField(blank=True, null=True)),
                ("description", models.CharField(blank=True, max_length=500)),
                ("comments", models.TextField(blank=True)),
                (
                    "cluster",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="nodes",
                        to="netbox_proxy.proxycluster",
                    ),
                ),
                (
                    "assigned_object_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="contenttypes.contenttype",
                        verbose_name="Assigned object type",
                    ),
                ),
            ],
            options={
                "verbose_name": "Proxy Node",
                "ordering": ("cluster", "name"),
            },
        ),
        migrations.AddConstraint(
            model_name="proxynode",
            constraint=models.UniqueConstraint(
                fields=("cluster", "name"),
                name="netbox_proxy_proxynode_unique_cluster_name",
            ),
        ),
        # ── ProxyVHost ────────────────────────────────────────────────────────
        migrations.CreateModel(
            name="ProxyVHost",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("custom_field_data", models.JSONField(blank=True, default=dict)),
                ("name", models.CharField(max_length=255)),
                ("server_names", models.TextField()),
                ("listen_port", models.PositiveIntegerField(default=80)),
                ("listen_ssl_port", models.PositiveIntegerField(default=443)),
                (
                    "ssl_mode",
                    models.CharField(
                        choices=[
                            ("off", "Off"),
                            ("on", "On"),
                            ("strict", "Strict"),
                        ],
                        default="off",
                        max_length=20,
                    ),
                ),
                ("is_enabled", models.BooleanField(default=True)),
                ("is_default_server", models.BooleanField(default=False)),
                ("access_log", models.CharField(blank=True, max_length=500)),
                ("error_log", models.CharField(blank=True, max_length=500)),
                ("custom_directives", models.TextField(blank=True)),
                ("description", models.CharField(blank=True, max_length=500)),
                ("comments", models.TextField(blank=True)),
                (
                    "cluster",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="vhosts",
                        to="netbox_proxy.proxycluster",
                    ),
                ),
                (
                    "ssl_certificate",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="vhosts",
                        to="netbox_proxy.proxysslcertificate",
                    ),
                ),
            ],
            options={
                "verbose_name": "Proxy VHost",
                "ordering": ("cluster", "name"),
            },
        ),
        migrations.AddConstraint(
            model_name="proxyvhost",
            constraint=models.UniqueConstraint(
                fields=("cluster", "name"),
                name="netbox_proxy_proxyvhost_unique_cluster_name",
            ),
        ),
        # ── ProxyUpstream ─────────────────────────────────────────────────────
        migrations.CreateModel(
            name="ProxyUpstream",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("custom_field_data", models.JSONField(blank=True, default=dict)),
                ("name", models.CharField(max_length=255)),
                (
                    "protocol",
                    models.CharField(
                        choices=[
                            ("http", "HTTP"),
                            ("https", "HTTPS"),
                            ("grpc", "gRPC"),
                            ("fastcgi", "FastCGI"),
                        ],
                        default="http",
                        max_length=20,
                    ),
                ),
                (
                    "balance",
                    models.CharField(
                        choices=[
                            ("round_robin", "Round Robin"),
                            ("least_conn", "Least Connections"),
                            ("ip_hash", "IP Hash"),
                            ("random", "Random"),
                        ],
                        default="round_robin",
                        max_length=20,
                    ),
                ),
                ("keepalive", models.PositiveIntegerField(default=0)),
                ("health_check_enabled", models.BooleanField(default=False)),
                ("health_check_path", models.CharField(blank=True, default="/health", max_length=500)),
                ("health_check_interval", models.PositiveIntegerField(default=5)),
                ("custom_directives", models.TextField(blank=True)),
                ("description", models.CharField(blank=True, max_length=500)),
                ("comments", models.TextField(blank=True)),
                (
                    "cluster",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="upstreams",
                        to="netbox_proxy.proxycluster",
                    ),
                ),
            ],
            options={
                "verbose_name": "Proxy Upstream",
                "ordering": ("cluster", "name"),
            },
        ),
        migrations.AddConstraint(
            model_name="proxyupstream",
            constraint=models.UniqueConstraint(
                fields=("cluster", "name"),
                name="netbox_proxy_proxyupstream_unique_cluster_name",
            ),
        ),
        # ── ProxyUpstreamServer ───────────────────────────────────────────────
        migrations.CreateModel(
            name="ProxyUpstreamServer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("custom_field_data", models.JSONField(blank=True, default=dict)),
                ("address", models.CharField(max_length=255)),
                ("weight", models.PositiveIntegerField(default=1)),
                ("max_fails", models.PositiveIntegerField(default=3)),
                ("fail_timeout", models.PositiveIntegerField(default=30)),
                ("enabled", models.BooleanField(default=True)),
                ("is_backup", models.BooleanField(default=False)),
                ("is_down", models.BooleanField(default=False)),
                ("description", models.CharField(blank=True, max_length=500)),
                ("comments", models.TextField(blank=True)),
                (
                    "upstream",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="servers",
                        to="netbox_proxy.proxyupstream",
                    ),
                ),
            ],
            options={
                "verbose_name": "Proxy Upstream Server",
                "ordering": ("upstream", "address"),
            },
        ),
        migrations.AddConstraint(
            model_name="proxyupstreamserver",
            constraint=models.UniqueConstraint(
                fields=("upstream", "address"),
                name="netbox_proxy_proxyupstreamserver_unique_upstream_address",
            ),
        ),
        # ── ProxyLocation ─────────────────────────────────────────────────────
        migrations.CreateModel(
            name="ProxyLocation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("custom_field_data", models.JSONField(blank=True, default=dict)),
                ("path", models.CharField(max_length=500)),
                (
                    "match_type",
                    models.CharField(
                        choices=[
                            ("prefix", "Prefix"),
                            ("exact", "Exact"),
                            ("regex", "Regex"),
                            ("regex_icase", "Regex (case-insensitive)"),
                        ],
                        default="prefix",
                        max_length=20,
                    ),
                ),
                ("proxy_pass_url", models.CharField(blank=True, max_length=500)),
                ("proxy_set_headers", models.JSONField(blank=True, default=dict)),
                ("sort_order", models.PositiveIntegerField(default=100)),
                ("custom_directives", models.TextField(blank=True)),
                ("description", models.CharField(blank=True, max_length=500)),
                ("comments", models.TextField(blank=True)),
                (
                    "vhost",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="locations",
                        to="netbox_proxy.proxyvhost",
                    ),
                ),
                (
                    "upstream",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="locations",
                        to="netbox_proxy.proxyupstream",
                    ),
                ),
                (
                    "rate_limit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="locations",
                        to="netbox_proxy.proxyratelimit",
                    ),
                ),
            ],
            options={
                "verbose_name": "Proxy Location",
                "ordering": ("vhost", "path"),
            },
        ),
        migrations.AddConstraint(
            model_name="proxylocation",
            constraint=models.UniqueConstraint(
                fields=("vhost", "path"),
                name="netbox_proxy_proxylocation_unique_vhost_path",
            ),
        ),
        # ── ProxyDeployment ───────────────────────────────────────────────────
        migrations.CreateModel(
            name="ProxyDeployment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("custom_field_data", models.JSONField(blank=True, default=dict)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("rendering", "Rendering"),
                            ("testing", "Testing"),
                            ("deploying", "Deploying"),
                            ("reloading", "Reloading"),
                            ("success", "Success"),
                            ("failed", "Failed"),
                            ("rolled_back", "Rolled Back"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("config_snapshot", models.TextField(blank=True)),
                ("previous_config", models.TextField(blank=True)),
                ("started_at", models.DateTimeField(blank=True, null=True)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("error_message", models.TextField(blank=True)),
                ("description", models.CharField(blank=True, max_length=500)),
                ("comments", models.TextField(blank=True)),
                (
                    "cluster",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="deployments",
                        to="netbox_proxy.proxycluster",
                    ),
                ),
                (
                    "node",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="deployments",
                        to="netbox_proxy.proxynode",
                    ),
                ),
                (
                    "initiated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "rpc_execution",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="proxy_deployments",
                        to="netbox_rpc.rpcexecution",
                    ),
                ),
            ],
            options={
                "verbose_name": "Proxy Deployment",
                "ordering": ("-created",),
            },
        ),
        # ── ProxyRateLimit vhost FK ───────────────────────────────────────────
        migrations.AddField(
            model_name="proxyratelimit",
            name="vhost",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="rate_limits",
                to="netbox_proxy.proxyvhost",
            ),
        ),
        # ── Indexes ───────────────────────────────────────────────────────────
        migrations.AddIndex(
            model_name="proxynode",
            index=models.Index(
                fields=["assigned_object_type", "assigned_object_id"],
                name="netbox_proxy_node_assigned_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="proxydeployment",
            index=models.Index(
                fields=["cluster", "status"],
                name="netbox_proxy_deployment_cluster_status_idx",
            ),
        ),
    ]
