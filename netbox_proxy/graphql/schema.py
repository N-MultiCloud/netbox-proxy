import strawberry
import strawberry_django

from .types import (
    ProxyClusterType,
    ProxyDeploymentType,
    ProxyLocationType,
    ProxyNodeType,
    ProxyRateLimitType,
    ProxySSLCertificateType,
    ProxyUpstreamServerType,
    ProxyUpstreamType,
    ProxyVHostType,
)


@strawberry.type(name="Query")
class NetBoxProxyQuery:
    proxy_cluster: ProxyClusterType = strawberry_django.field()
    proxy_cluster_list: list[ProxyClusterType] = strawberry_django.field()

    proxy_node: ProxyNodeType = strawberry_django.field()
    proxy_node_list: list[ProxyNodeType] = strawberry_django.field()

    proxy_vhost: ProxyVHostType = strawberry_django.field()
    proxy_vhost_list: list[ProxyVHostType] = strawberry_django.field()

    proxy_upstream: ProxyUpstreamType = strawberry_django.field()
    proxy_upstream_list: list[ProxyUpstreamType] = strawberry_django.field()

    proxy_upstream_server: ProxyUpstreamServerType = strawberry_django.field()
    proxy_upstream_server_list: list[ProxyUpstreamServerType] = strawberry_django.field()

    proxy_ssl_certificate: ProxySSLCertificateType = strawberry_django.field()
    proxy_ssl_certificate_list: list[ProxySSLCertificateType] = strawberry_django.field()

    proxy_rate_limit: ProxyRateLimitType = strawberry_django.field()
    proxy_rate_limit_list: list[ProxyRateLimitType] = strawberry_django.field()

    proxy_location: ProxyLocationType = strawberry_django.field()
    proxy_location_list: list[ProxyLocationType] = strawberry_django.field()

    proxy_deployment: ProxyDeploymentType = strawberry_django.field()
    proxy_deployment_list: list[ProxyDeploymentType] = strawberry_django.field()
