import strawberry_django
from netbox.graphql.filters import NetBoxModelFilter

from netbox_proxy import models


@strawberry_django.filter_type(models.ProxyCluster, lookups=True)
class ProxyClusterFilter(NetBoxModelFilter):
    pass


@strawberry_django.filter_type(models.ProxyNode, lookups=True)
class ProxyNodeFilter(NetBoxModelFilter):
    pass


@strawberry_django.filter_type(models.ProxyVHost, lookups=True)
class ProxyVHostFilter(NetBoxModelFilter):
    pass


@strawberry_django.filter_type(models.ProxyUpstream, lookups=True)
class ProxyUpstreamFilter(NetBoxModelFilter):
    pass


@strawberry_django.filter_type(models.ProxyUpstreamServer, lookups=True)
class ProxyUpstreamServerFilter(NetBoxModelFilter):
    pass


@strawberry_django.filter_type(models.ProxySSLCertificate, lookups=True)
class ProxySSLCertificateFilter(NetBoxModelFilter):
    pass


@strawberry_django.filter_type(models.ProxyRateLimit, lookups=True)
class ProxyRateLimitFilter(NetBoxModelFilter):
    pass


@strawberry_django.filter_type(models.ProxyLocation, lookups=True)
class ProxyLocationFilter(NetBoxModelFilter):
    pass


@strawberry_django.filter_type(models.ProxyDeployment, lookups=True)
class ProxyDeploymentFilter(NetBoxModelFilter):
    pass
