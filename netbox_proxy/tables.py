import django_tables2 as tables
from netbox.tables import NetBoxTable, columns

from .models import (
    ProxyCluster,
    ProxyDeployment,
    ProxyLocation,
    ProxyNode,
    ProxyRateLimit,
    ProxySSLCertificate,
    ProxyUpstream,
    ProxyUpstreamServer,
    ProxyVHost,
)


class ProxyClusterTable(NetBoxTable):
    name = tables.Column(linkify=True)
    node_count = tables.Column(verbose_name="Nodes")

    class Meta(NetBoxTable.Meta):
        model = ProxyCluster
        fields = ("pk", "id", "name", "description", "node_count", "tags", "actions")
        default_columns = ("name", "description", "node_count")


class ProxyNodeTable(NetBoxTable):
    name = tables.Column(linkify=True)
    cluster = tables.Column(linkify=True)
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name="Assigned Object",
    )
    is_active = columns.BooleanColumn()

    class Meta(NetBoxTable.Meta):
        model = ProxyNode
        fields = ("pk", "id", "cluster", "name", "assigned_object", "management_ip", "is_active", "description", "tags", "actions")
        default_columns = ("cluster", "name", "assigned_object", "management_ip", "is_active")


class ProxyVHostTable(NetBoxTable):
    name = tables.Column(linkify=True)
    cluster = tables.Column(linkify=True)
    ssl_mode = columns.ChoiceFieldColumn()
    ssl_certificate = tables.Column(linkify=True)
    is_enabled = columns.BooleanColumn()

    class Meta(NetBoxTable.Meta):
        model = ProxyVHost
        fields = (
            "pk",
            "id",
            "cluster",
            "name",
            "server_names",
            "listen_port",
            "ssl_mode",
            "ssl_certificate",
            "is_enabled",
            "tags",
            "actions",
        )
        default_columns = ("cluster", "name", "server_names", "listen_port", "ssl_mode", "is_enabled")


class ProxyUpstreamTable(NetBoxTable):
    name = tables.Column(linkify=True)
    cluster = tables.Column(linkify=True)
    protocol = columns.ChoiceFieldColumn()
    balance = columns.ChoiceFieldColumn()
    health_check_enabled = columns.BooleanColumn()

    class Meta(NetBoxTable.Meta):
        model = ProxyUpstream
        fields = (
            "pk",
            "id",
            "cluster",
            "name",
            "protocol",
            "balance",
            "keepalive",
            "health_check_enabled",
            "description",
            "tags",
            "actions",
        )
        default_columns = ("cluster", "name", "protocol", "balance", "health_check_enabled")


class ProxyUpstreamServerTable(NetBoxTable):
    upstream = tables.Column(linkify=True)
    enabled = columns.BooleanColumn()
    is_backup = columns.BooleanColumn()
    is_down = columns.BooleanColumn()

    class Meta(NetBoxTable.Meta):
        model = ProxyUpstreamServer
        fields = (
            "pk",
            "id",
            "upstream",
            "address",
            "weight",
            "max_fails",
            "fail_timeout",
            "enabled",
            "is_backup",
            "is_down",
            "tags",
            "actions",
        )
        default_columns = ("upstream", "address", "weight", "enabled", "is_backup", "is_down")


class ProxySSLCertificateTable(NetBoxTable):
    name = tables.Column(linkify=True)
    provider = columns.ChoiceFieldColumn()
    auto_renew = columns.BooleanColumn()

    class Meta(NetBoxTable.Meta):
        model = ProxySSLCertificate
        fields = (
            "pk",
            "id",
            "name",
            "provider",
            "domain",
            "cert_path",
            "auto_renew",
            "expires_at",
            "tags",
            "actions",
        )
        default_columns = ("name", "provider", "domain", "auto_renew", "expires_at")


class ProxyRateLimitTable(NetBoxTable):
    name = tables.Column(linkify=True)
    nodelay = columns.BooleanColumn()

    class Meta(NetBoxTable.Meta):
        model = ProxyRateLimit
        fields = ("pk", "id", "name", "zone_name", "rate", "burst", "nodelay", "description", "tags", "actions")
        default_columns = ("name", "zone_name", "rate", "burst", "nodelay")


class ProxyLocationTable(NetBoxTable):
    vhost = tables.Column(linkify=True)
    upstream = tables.Column(linkify=True)
    match_type = columns.ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        model = ProxyLocation
        fields = (
            "pk",
            "id",
            "vhost",
            "path",
            "match_type",
            "upstream",
            "rate_limit",
            "sort_order",
            "tags",
            "actions",
        )
        default_columns = ("vhost", "path", "match_type", "upstream", "sort_order")


class ProxyDeploymentTable(NetBoxTable):
    cluster = tables.Column(linkify=True)
    node = tables.Column(linkify=True)
    status = columns.ChoiceFieldColumn()
    initiated_by = tables.Column()
    rpc_execution = tables.Column(linkify=True, verbose_name="RPC Execution")

    class Meta(NetBoxTable.Meta):
        model = ProxyDeployment
        fields = (
            "pk",
            "id",
            "cluster",
            "node",
            "status",
            "initiated_by",
            "rpc_execution",
            "started_at",
            "completed_at",
            "created",
            "tags",
            "actions",
        )
        default_columns = ("cluster", "node", "status", "initiated_by", "rpc_execution", "started_at", "created")
