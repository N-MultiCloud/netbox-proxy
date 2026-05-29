from django.urls import include, path
from utilities.urls import get_model_urls

from . import views  # noqa: F401 - imports register @register_model_view routes

_MODEL_ROUTES = (
    ("proxycluster", "clusters"),
    ("proxynode", "nodes"),
    ("proxyvhost", "vhosts"),
    ("proxyupstream", "upstreams"),
    ("proxyupstreamserver", "upstream-servers"),
    ("proxysslcertificate", "ssl-certificates"),
    ("proxyratelimit", "rate-limits"),
    ("proxylocation", "locations"),
    ("proxydeployment", "deployments"),
)

urlpatterns = []

for _model_name, _slug in _MODEL_ROUTES:
    urlpatterns += [
        path(
            f"{_slug}/",
            include(get_model_urls("netbox_proxy", _model_name, detail=False)),
        ),
        path(
            f"{_slug}/<int:pk>/", include(get_model_urls("netbox_proxy", _model_name))
        ),
    ]
