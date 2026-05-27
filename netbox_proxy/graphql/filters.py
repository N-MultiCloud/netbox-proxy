import strawberry_django
from netbox.graphql.filter_mixins import autotype_decorator, BaseFilterMixin

from netbox_proxy import filtersets, models


@strawberry_django.filter_type(models.ProxyCluster, lookups=True)
@autotype_decorator(filtersets.ProxyClusterFilterSet)
class ProxyClusterFilter(BaseFilterMixin):
    pass


@strawberry_django.filter_type(models.ProxyNode, lookups=True)
@autotype_decorator(filtersets.ProxyNodeFilterSet)
class ProxyNodeFilter(BaseFilterMixin):
    pass


@strawberry_django.filter_type(models.ProxyVHost, lookups=True)
@autotype_decorator(filtersets.ProxyVHostFilterSet)
class ProxyVHostFilter(BaseFilterMixin):
    pass


@strawberry_django.filter_type(models.ProxyUpstream, lookups=True)
@autotype_decorator(filtersets.ProxyUpstreamFilterSet)
class ProxyUpstreamFilter(BaseFilterMixin):
    pass


@strawberry_django.filter_type(models.ProxyUpstreamServer, lookups=True)
@autotype_decorator(filtersets.ProxyUpstreamServerFilterSet)
class ProxyUpstreamServerFilter(BaseFilterMixin):
    pass


@strawberry_django.filter_type(models.ProxySSLCertificate, lookups=True)
@autotype_decorator(filtersets.ProxySSLCertificateFilterSet)
class ProxySSLCertificateFilter(BaseFilterMixin):
    pass


@strawberry_django.filter_type(models.ProxyRateLimit, lookups=True)
@autotype_decorator(filtersets.ProxyRateLimitFilterSet)
class ProxyRateLimitFilter(BaseFilterMixin):
    pass


@strawberry_django.filter_type(models.ProxyLocation, lookups=True)
@autotype_decorator(filtersets.ProxyLocationFilterSet)
class ProxyLocationFilter(BaseFilterMixin):
    pass


@strawberry_django.filter_type(models.ProxyDeployment, lookups=True)
@autotype_decorator(filtersets.ProxyDeploymentFilterSet)
class ProxyDeploymentFilter(BaseFilterMixin):
    pass
