from netbox.object_actions import AddObject, BulkDelete, BulkExport
from netbox.views import generic
from utilities.views import register_model_view

from . import filtersets, forms, models, tables

LIST_ACTIONS = (AddObject, BulkExport, BulkDelete)


# ── ProxyCluster ─────────────────────────────────────────────────────────────


@register_model_view(models.ProxyCluster, "list", path="", detail=False)
class ProxyClusterListView(generic.ObjectListView):
    queryset = models.ProxyCluster.objects.all()
    table = tables.ProxyClusterTable
    filterset = filtersets.ProxyClusterFilterSet
    filterset_form = forms.ProxyClusterFilterForm
    actions = LIST_ACTIONS


@register_model_view(models.ProxyCluster)
class ProxyClusterView(generic.ObjectView):
    queryset = models.ProxyCluster.objects.all()


@register_model_view(models.ProxyCluster, "add", detail=False)
@register_model_view(models.ProxyCluster, "edit")
class ProxyClusterEditView(generic.ObjectEditView):
    queryset = models.ProxyCluster.objects.all()
    form = forms.ProxyClusterForm


@register_model_view(models.ProxyCluster, "delete")
class ProxyClusterDeleteView(generic.ObjectDeleteView):
    queryset = models.ProxyCluster.objects.all()


@register_model_view(models.ProxyCluster, "bulk_delete", path="delete", detail=False)
class ProxyClusterBulkDeleteView(generic.BulkDeleteView):
    queryset = models.ProxyCluster.objects.all()
    table = tables.ProxyClusterTable


# ── ProxyNode ─────────────────────────────────────────────────────────────────


@register_model_view(models.ProxyNode, "list", path="", detail=False)
class ProxyNodeListView(generic.ObjectListView):
    queryset = models.ProxyNode.objects.select_related("cluster")
    table = tables.ProxyNodeTable
    filterset = filtersets.ProxyNodeFilterSet
    filterset_form = forms.ProxyNodeFilterForm
    actions = LIST_ACTIONS


@register_model_view(models.ProxyNode)
class ProxyNodeView(generic.ObjectView):
    queryset = models.ProxyNode.objects.select_related("cluster")


@register_model_view(models.ProxyNode, "add", detail=False)
@register_model_view(models.ProxyNode, "edit")
class ProxyNodeEditView(generic.ObjectEditView):
    queryset = models.ProxyNode.objects.all()
    form = forms.ProxyNodeForm


@register_model_view(models.ProxyNode, "delete")
class ProxyNodeDeleteView(generic.ObjectDeleteView):
    queryset = models.ProxyNode.objects.all()


@register_model_view(models.ProxyNode, "bulk_delete", path="delete", detail=False)
class ProxyNodeBulkDeleteView(generic.BulkDeleteView):
    queryset = models.ProxyNode.objects.all()
    table = tables.ProxyNodeTable


# ── ProxyVHost ────────────────────────────────────────────────────────────────


@register_model_view(models.ProxyVHost, "list", path="", detail=False)
class ProxyVHostListView(generic.ObjectListView):
    queryset = models.ProxyVHost.objects.select_related("cluster", "ssl_certificate")
    table = tables.ProxyVHostTable
    filterset = filtersets.ProxyVHostFilterSet
    filterset_form = forms.ProxyVHostFilterForm
    actions = LIST_ACTIONS


@register_model_view(models.ProxyVHost)
class ProxyVHostView(generic.ObjectView):
    queryset = models.ProxyVHost.objects.select_related("cluster", "ssl_certificate")


@register_model_view(models.ProxyVHost, "add", detail=False)
@register_model_view(models.ProxyVHost, "edit")
class ProxyVHostEditView(generic.ObjectEditView):
    queryset = models.ProxyVHost.objects.all()
    form = forms.ProxyVHostForm


@register_model_view(models.ProxyVHost, "delete")
class ProxyVHostDeleteView(generic.ObjectDeleteView):
    queryset = models.ProxyVHost.objects.all()


@register_model_view(models.ProxyVHost, "bulk_delete", path="delete", detail=False)
class ProxyVHostBulkDeleteView(generic.BulkDeleteView):
    queryset = models.ProxyVHost.objects.all()
    table = tables.ProxyVHostTable


# ── ProxyUpstream ─────────────────────────────────────────────────────────────


@register_model_view(models.ProxyUpstream, "list", path="", detail=False)
class ProxyUpstreamListView(generic.ObjectListView):
    queryset = models.ProxyUpstream.objects.select_related("cluster")
    table = tables.ProxyUpstreamTable
    filterset = filtersets.ProxyUpstreamFilterSet
    filterset_form = forms.ProxyUpstreamFilterForm
    actions = LIST_ACTIONS


@register_model_view(models.ProxyUpstream)
class ProxyUpstreamView(generic.ObjectView):
    queryset = models.ProxyUpstream.objects.select_related("cluster")


@register_model_view(models.ProxyUpstream, "add", detail=False)
@register_model_view(models.ProxyUpstream, "edit")
class ProxyUpstreamEditView(generic.ObjectEditView):
    queryset = models.ProxyUpstream.objects.all()
    form = forms.ProxyUpstreamForm


@register_model_view(models.ProxyUpstream, "delete")
class ProxyUpstreamDeleteView(generic.ObjectDeleteView):
    queryset = models.ProxyUpstream.objects.all()


@register_model_view(models.ProxyUpstream, "bulk_delete", path="delete", detail=False)
class ProxyUpstreamBulkDeleteView(generic.BulkDeleteView):
    queryset = models.ProxyUpstream.objects.all()
    table = tables.ProxyUpstreamTable


# ── ProxyUpstreamServer ───────────────────────────────────────────────────────


@register_model_view(models.ProxyUpstreamServer, "list", path="", detail=False)
class ProxyUpstreamServerListView(generic.ObjectListView):
    queryset = models.ProxyUpstreamServer.objects.select_related("upstream__cluster")
    table = tables.ProxyUpstreamServerTable
    filterset = filtersets.ProxyUpstreamServerFilterSet
    filterset_form = forms.ProxyUpstreamServerFilterForm
    actions = LIST_ACTIONS


@register_model_view(models.ProxyUpstreamServer)
class ProxyUpstreamServerView(generic.ObjectView):
    queryset = models.ProxyUpstreamServer.objects.select_related("upstream__cluster")


@register_model_view(models.ProxyUpstreamServer, "add", detail=False)
@register_model_view(models.ProxyUpstreamServer, "edit")
class ProxyUpstreamServerEditView(generic.ObjectEditView):
    queryset = models.ProxyUpstreamServer.objects.all()
    form = forms.ProxyUpstreamServerForm


@register_model_view(models.ProxyUpstreamServer, "delete")
class ProxyUpstreamServerDeleteView(generic.ObjectDeleteView):
    queryset = models.ProxyUpstreamServer.objects.all()


@register_model_view(
    models.ProxyUpstreamServer,
    "bulk_delete",
    path="delete",
    detail=False,
)
class ProxyUpstreamServerBulkDeleteView(generic.BulkDeleteView):
    queryset = models.ProxyUpstreamServer.objects.all()
    table = tables.ProxyUpstreamServerTable


# ── ProxySSLCertificate ───────────────────────────────────────────────────────


@register_model_view(models.ProxySSLCertificate, "list", path="", detail=False)
class ProxySSLCertificateListView(generic.ObjectListView):
    queryset = models.ProxySSLCertificate.objects.all()
    table = tables.ProxySSLCertificateTable
    filterset = filtersets.ProxySSLCertificateFilterSet
    filterset_form = forms.ProxySSLCertificateFilterForm
    actions = LIST_ACTIONS


@register_model_view(models.ProxySSLCertificate)
class ProxySSLCertificateView(generic.ObjectView):
    queryset = models.ProxySSLCertificate.objects.all()


@register_model_view(models.ProxySSLCertificate, "add", detail=False)
@register_model_view(models.ProxySSLCertificate, "edit")
class ProxySSLCertificateEditView(generic.ObjectEditView):
    queryset = models.ProxySSLCertificate.objects.all()
    form = forms.ProxySSLCertificateForm


@register_model_view(models.ProxySSLCertificate, "delete")
class ProxySSLCertificateDeleteView(generic.ObjectDeleteView):
    queryset = models.ProxySSLCertificate.objects.all()


@register_model_view(
    models.ProxySSLCertificate,
    "bulk_delete",
    path="delete",
    detail=False,
)
class ProxySSLCertificateBulkDeleteView(generic.BulkDeleteView):
    queryset = models.ProxySSLCertificate.objects.all()
    table = tables.ProxySSLCertificateTable


# ── ProxyRateLimit ────────────────────────────────────────────────────────────


@register_model_view(models.ProxyRateLimit, "list", path="", detail=False)
class ProxyRateLimitListView(generic.ObjectListView):
    queryset = models.ProxyRateLimit.objects.all()
    table = tables.ProxyRateLimitTable
    filterset = filtersets.ProxyRateLimitFilterSet
    filterset_form = forms.ProxyRateLimitFilterForm
    actions = LIST_ACTIONS


@register_model_view(models.ProxyRateLimit)
class ProxyRateLimitView(generic.ObjectView):
    queryset = models.ProxyRateLimit.objects.all()


@register_model_view(models.ProxyRateLimit, "add", detail=False)
@register_model_view(models.ProxyRateLimit, "edit")
class ProxyRateLimitEditView(generic.ObjectEditView):
    queryset = models.ProxyRateLimit.objects.all()
    form = forms.ProxyRateLimitForm


@register_model_view(models.ProxyRateLimit, "delete")
class ProxyRateLimitDeleteView(generic.ObjectDeleteView):
    queryset = models.ProxyRateLimit.objects.all()


@register_model_view(models.ProxyRateLimit, "bulk_delete", path="delete", detail=False)
class ProxyRateLimitBulkDeleteView(generic.BulkDeleteView):
    queryset = models.ProxyRateLimit.objects.all()
    table = tables.ProxyRateLimitTable


# ── ProxyLocation ─────────────────────────────────────────────────────────────


@register_model_view(models.ProxyLocation, "list", path="", detail=False)
class ProxyLocationListView(generic.ObjectListView):
    queryset = models.ProxyLocation.objects.select_related(
        "vhost__cluster", "upstream", "rate_limit"
    )
    table = tables.ProxyLocationTable
    filterset = filtersets.ProxyLocationFilterSet
    filterset_form = forms.ProxyLocationFilterForm
    actions = LIST_ACTIONS


@register_model_view(models.ProxyLocation)
class ProxyLocationView(generic.ObjectView):
    queryset = models.ProxyLocation.objects.select_related(
        "vhost__cluster", "upstream", "rate_limit"
    )


@register_model_view(models.ProxyLocation, "add", detail=False)
@register_model_view(models.ProxyLocation, "edit")
class ProxyLocationEditView(generic.ObjectEditView):
    queryset = models.ProxyLocation.objects.all()
    form = forms.ProxyLocationForm


@register_model_view(models.ProxyLocation, "delete")
class ProxyLocationDeleteView(generic.ObjectDeleteView):
    queryset = models.ProxyLocation.objects.all()


@register_model_view(models.ProxyLocation, "bulk_delete", path="delete", detail=False)
class ProxyLocationBulkDeleteView(generic.BulkDeleteView):
    queryset = models.ProxyLocation.objects.all()
    table = tables.ProxyLocationTable


# ── ProxyDeployment ───────────────────────────────────────────────────────────


@register_model_view(models.ProxyDeployment, "list", path="", detail=False)
class ProxyDeploymentListView(generic.ObjectListView):
    queryset = models.ProxyDeployment.objects.select_related("cluster", "node", "initiated_by", "rpc_execution")
    table = tables.ProxyDeploymentTable
    filterset = filtersets.ProxyDeploymentFilterSet
    filterset_form = forms.ProxyDeploymentFilterForm
    actions = LIST_ACTIONS


@register_model_view(models.ProxyDeployment)
class ProxyDeploymentView(generic.ObjectView):
    queryset = models.ProxyDeployment.objects.select_related(
        "cluster", "initiated_by", "rpc_execution"
    )


@register_model_view(models.ProxyDeployment, "add", detail=False)
@register_model_view(models.ProxyDeployment, "edit")
class ProxyDeploymentEditView(generic.ObjectEditView):
    queryset = models.ProxyDeployment.objects.all()
    form = forms.ProxyDeploymentForm


@register_model_view(models.ProxyDeployment, "delete")
class ProxyDeploymentDeleteView(generic.ObjectDeleteView):
    queryset = models.ProxyDeployment.objects.all()


@register_model_view(models.ProxyDeployment, "bulk_delete", path="delete", detail=False)
class ProxyDeploymentBulkDeleteView(generic.BulkDeleteView):
    queryset = models.ProxyDeployment.objects.all()
    table = tables.ProxyDeploymentTable
