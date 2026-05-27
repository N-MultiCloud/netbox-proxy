import django_filters
from netbox.filtersets import NetBoxModelFilterSet

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


class ProxyClusterFilterSet(NetBoxModelFilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = ProxyCluster
        fields = ("name", "description")


class ProxyNodeFilterSet(NetBoxModelFilterSet):
    cluster_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ProxyCluster.objects.all(),
        field_name="cluster",
        label="Cluster (ID)",
    )
    name = django_filters.CharFilter(lookup_expr="icontains")
    management_ip = django_filters.CharFilter(lookup_expr="icontains")
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = ProxyNode
        fields = ("cluster_id", "name", "management_ip", "is_active")


class ProxyVHostFilterSet(NetBoxModelFilterSet):
    cluster_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ProxyCluster.objects.all(),
        field_name="cluster",
        label="Cluster (ID)",
    )
    name = django_filters.CharFilter(lookup_expr="icontains")
    server_names = django_filters.CharFilter(lookup_expr="icontains")
    ssl_mode = django_filters.MultipleChoiceFilter(
        choices=[
            ("off", "Off"),
            ("on", "On"),
            ("strict", "Strict"),
        ]
    )
    is_enabled = django_filters.BooleanFilter()

    class Meta:
        model = ProxyVHost
        fields = ("cluster_id", "name", "server_names", "ssl_mode", "listen_port", "is_enabled")


class ProxyUpstreamFilterSet(NetBoxModelFilterSet):
    cluster_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ProxyCluster.objects.all(),
        field_name="cluster",
        label="Cluster (ID)",
    )
    name = django_filters.CharFilter(lookup_expr="icontains")
    protocol = django_filters.MultipleChoiceFilter(
        choices=[
            ("http", "HTTP"),
            ("https", "HTTPS"),
            ("grpc", "gRPC"),
            ("fastcgi", "FastCGI"),
        ]
    )
    balance = django_filters.MultipleChoiceFilter(
        choices=[
            ("round_robin", "Round Robin"),
            ("least_conn", "Least Connections"),
            ("ip_hash", "IP Hash"),
            ("random", "Random"),
        ]
    )
    health_check_enabled = django_filters.BooleanFilter()

    class Meta:
        model = ProxyUpstream
        fields = ("cluster_id", "name", "protocol", "balance", "health_check_enabled")


class ProxyUpstreamServerFilterSet(NetBoxModelFilterSet):
    upstream_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ProxyUpstream.objects.all(),
        field_name="upstream",
        label="Upstream (ID)",
    )
    address = django_filters.CharFilter(lookup_expr="icontains")
    enabled = django_filters.BooleanFilter()
    is_backup = django_filters.BooleanFilter()
    is_down = django_filters.BooleanFilter()

    class Meta:
        model = ProxyUpstreamServer
        fields = ("upstream_id", "address", "enabled", "is_backup", "is_down")


class ProxySSLCertificateFilterSet(NetBoxModelFilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    domain = django_filters.CharFilter(lookup_expr="icontains")
    provider = django_filters.MultipleChoiceFilter(
        choices=[
            ("manual", "Manual"),
            ("letsencrypt", "Let's Encrypt"),
            ("selfsigned", "Self-Signed"),
        ]
    )
    auto_renew = django_filters.BooleanFilter()

    class Meta:
        model = ProxySSLCertificate
        fields = ("name", "provider", "domain", "auto_renew")


class ProxyRateLimitFilterSet(NetBoxModelFilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    vhost_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ProxyVHost.objects.all(),
        field_name="vhost",
        label="VHost (ID)",
    )
    zone_name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = ProxyRateLimit
        fields = ("name", "vhost_id", "zone_name")


class ProxyLocationFilterSet(NetBoxModelFilterSet):
    vhost_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ProxyVHost.objects.all(),
        field_name="vhost",
        label="VHost (ID)",
    )
    upstream_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ProxyUpstream.objects.all(),
        field_name="upstream",
        label="Upstream (ID)",
    )
    path = django_filters.CharFilter(lookup_expr="icontains")
    match_type = django_filters.MultipleChoiceFilter(
        choices=[
            ("prefix", "Prefix"),
            ("exact", "Exact"),
            ("regex", "Regex"),
            ("regex_icase", "Regex (case-insensitive)"),
        ]
    )

    class Meta:
        model = ProxyLocation
        fields = ("vhost_id", "upstream_id", "path", "match_type")


class ProxyDeploymentFilterSet(NetBoxModelFilterSet):
    cluster_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ProxyCluster.objects.all(),
        field_name="cluster",
        label="Cluster (ID)",
    )
    node_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ProxyNode.objects.all(),
        field_name="node",
        label="Node (ID)",
    )
    status = django_filters.MultipleChoiceFilter(
        choices=[
            ("pending", "Pending"),
            ("rendering", "Rendering"),
            ("testing", "Testing"),
            ("deploying", "Deploying"),
            ("reloading", "Reloading"),
            ("success", "Success"),
            ("failed", "Failed"),
            ("rolled_back", "Rolled Back"),
        ]
    )

    class Meta:
        model = ProxyDeployment
        fields = ("cluster_id", "node_id", "status")
