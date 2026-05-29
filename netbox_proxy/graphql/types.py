import strawberry_django
from netbox.graphql.types import NetBoxObjectType

from netbox_proxy import models

from .filters import (
    ProxyClusterFilter,
    ProxyDeploymentFilter,
    ProxyLocationFilter,
    ProxyNodeFilter,
    ProxyRateLimitFilter,
    ProxySSLCertificateFilter,
    ProxyUpstreamFilter,
    ProxyUpstreamServerFilter,
    ProxyVHostFilter,
)


@strawberry_django.type(
    models.ProxyCluster, fields="__all__", filters=ProxyClusterFilter
)
class ProxyClusterType(NetBoxObjectType):
    pass


@strawberry_django.type(models.ProxyNode, fields="__all__", filters=ProxyNodeFilter)
class ProxyNodeType(NetBoxObjectType):
    pass


@strawberry_django.type(models.ProxyVHost, fields="__all__", filters=ProxyVHostFilter)
class ProxyVHostType(NetBoxObjectType):
    pass


@strawberry_django.type(
    models.ProxyUpstream, fields="__all__", filters=ProxyUpstreamFilter
)
class ProxyUpstreamType(NetBoxObjectType):
    pass


@strawberry_django.type(
    models.ProxyUpstreamServer, fields="__all__", filters=ProxyUpstreamServerFilter
)
class ProxyUpstreamServerType(NetBoxObjectType):
    pass


@strawberry_django.type(
    models.ProxySSLCertificate, fields="__all__", filters=ProxySSLCertificateFilter
)
class ProxySSLCertificateType(NetBoxObjectType):
    pass


@strawberry_django.type(
    models.ProxyRateLimit, fields="__all__", filters=ProxyRateLimitFilter
)
class ProxyRateLimitType(NetBoxObjectType):
    pass


@strawberry_django.type(
    models.ProxyLocation, fields="__all__", filters=ProxyLocationFilter
)
class ProxyLocationType(NetBoxObjectType):
    pass


@strawberry_django.type(
    models.ProxyDeployment, fields="__all__", filters=ProxyDeploymentFilter
)
class ProxyDeploymentType(NetBoxObjectType):
    pass
