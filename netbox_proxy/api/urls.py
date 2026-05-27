from netbox.api.routers import NetBoxRouter

from . import views

router = NetBoxRouter()
router.register("clusters", views.ProxyClusterViewSet)
router.register("nodes", views.ProxyNodeViewSet)
router.register("vhosts", views.ProxyVHostViewSet)
router.register("upstreams", views.ProxyUpstreamViewSet)
router.register("upstream-servers", views.ProxyUpstreamServerViewSet)
router.register("ssl-certificates", views.ProxySSLCertificateViewSet)
router.register("rate-limits", views.ProxyRateLimitViewSet)
router.register("locations", views.ProxyLocationViewSet)
router.register("deployments", views.ProxyDeploymentViewSet)

app_name = "netbox_proxy-api"
urlpatterns = router.urls
