from netbox.search import SearchIndex, register_search

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


@register_search
class ProxyClusterIndex(SearchIndex):
    model = ProxyCluster
    fields = (
        ("name", 100),
        ("description", 500),
        ("comments", 5000),
    )
    display_attrs = ("description",)


@register_search
class ProxyNodeIndex(SearchIndex):
    model = ProxyNode
    fields = (
        ("name", 100),
        ("management_ip", 200),
        ("description", 500),
        ("comments", 5000),
    )
    display_attrs = ("cluster", "description")


@register_search
class ProxyVHostIndex(SearchIndex):
    model = ProxyVHost
    fields = (
        ("name", 100),
        ("server_names", 200),
        ("description", 500),
        ("comments", 5000),
    )
    display_attrs = ("cluster", "server_names")


@register_search
class ProxyUpstreamIndex(SearchIndex):
    model = ProxyUpstream
    fields = (
        ("name", 100),
        ("description", 500),
        ("comments", 5000),
    )
    display_attrs = ("cluster", "protocol", "balance")


@register_search
class ProxyUpstreamServerIndex(SearchIndex):
    model = ProxyUpstreamServer
    fields = (
        ("address", 100),
        ("description", 500),
        ("comments", 5000),
    )
    display_attrs = ("upstream", "address")


@register_search
class ProxySSLCertificateIndex(SearchIndex):
    model = ProxySSLCertificate
    fields = (
        ("name", 100),
        ("domain", 200),
        ("description", 500),
        ("comments", 5000),
    )
    display_attrs = ("domain", "provider")


@register_search
class ProxyRateLimitIndex(SearchIndex):
    model = ProxyRateLimit
    fields = (
        ("name", 100),
        ("zone_name", 200),
        ("rate", 200),
        ("description", 500),
        ("comments", 5000),
    )
    display_attrs = ("rate", "burst")


@register_search
class ProxyLocationIndex(SearchIndex):
    model = ProxyLocation
    fields = (
        ("path", 100),
        ("description", 500),
        ("comments", 5000),
    )
    display_attrs = ("vhost", "path", "match_type")


@register_search
class ProxyDeploymentIndex(SearchIndex):
    model = ProxyDeployment
    fields = (
        ("description", 500),
        ("comments", 5000),
    )
    display_attrs = ("cluster", "status")
