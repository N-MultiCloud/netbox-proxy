from django.urls import path
from utilities.urls import get_model_urls

from . import views

urlpatterns = [
    # ProxyCluster
    path("clusters/", views.ProxyClusterListView.as_view(), name="proxycluster_list"),
    *get_model_urls("netbox_proxy", "proxycluster"),

    # ProxyNode
    path("nodes/", views.ProxyNodeListView.as_view(), name="proxynode_list"),
    *get_model_urls("netbox_proxy", "proxynode"),

    # ProxyVHost
    path("vhosts/", views.ProxyVHostListView.as_view(), name="proxyvhost_list"),
    *get_model_urls("netbox_proxy", "proxyvhost"),

    # ProxyUpstream
    path("upstreams/", views.ProxyUpstreamListView.as_view(), name="proxyupstream_list"),
    *get_model_urls("netbox_proxy", "proxyupstream"),

    # ProxyUpstreamServer
    path(
        "upstream-servers/",
        views.ProxyUpstreamServerListView.as_view(),
        name="proxyupstreamserver_list",
    ),
    *get_model_urls("netbox_proxy", "proxyupstreamserver"),

    # ProxySSLCertificate
    path(
        "ssl-certificates/",
        views.ProxySSLCertificateListView.as_view(),
        name="proxysslcertificate_list",
    ),
    *get_model_urls("netbox_proxy", "proxysslcertificate"),

    # ProxyRateLimit
    path("rate-limits/", views.ProxyRateLimitListView.as_view(), name="proxyratelimit_list"),
    *get_model_urls("netbox_proxy", "proxyratelimit"),

    # ProxyLocation
    path("locations/", views.ProxyLocationListView.as_view(), name="proxylocation_list"),
    *get_model_urls("netbox_proxy", "proxylocation"),

    # ProxyDeployment
    path("deployments/", views.ProxyDeploymentListView.as_view(), name="proxydeployment_list"),
    *get_model_urls("netbox_proxy", "proxydeployment"),
]
