from netbox.views import generic

from . import filtersets, forms, models, tables


# ── ProxyCluster ─────────────────────────────────────────────────────────────

class ProxyClusterListView(generic.ObjectListView):
    queryset = models.ProxyCluster.objects.all()
    table = tables.ProxyClusterTable
    filterset = filtersets.ProxyClusterFilterSet
    filterset_form = forms.ProxyClusterFilterForm


class ProxyClusterView(generic.ObjectView):
    queryset = models.ProxyCluster.objects.all()


class ProxyClusterEditView(generic.ObjectEditView):
    queryset = models.ProxyCluster.objects.all()
    form = forms.ProxyClusterForm


class ProxyClusterDeleteView(generic.ObjectDeleteView):
    queryset = models.ProxyCluster.objects.all()


class ProxyClusterBulkDeleteView(generic.BulkDeleteView):
    queryset = models.ProxyCluster.objects.all()
    table = tables.ProxyClusterTable


# ── ProxyNode ─────────────────────────────────────────────────────────────────

class ProxyNodeListView(generic.ObjectListView):
    queryset = models.ProxyNode.objects.select_related("cluster")
    table = tables.ProxyNodeTable
    filterset = filtersets.ProxyNodeFilterSet
    filterset_form = forms.ProxyNodeFilterForm


class ProxyNodeView(generic.ObjectView):
    queryset = models.ProxyNode.objects.select_related("cluster")


class ProxyNodeEditView(generic.ObjectEditView):
    queryset = models.ProxyNode.objects.all()
    form = forms.ProxyNodeForm


class ProxyNodeDeleteView(generic.ObjectDeleteView):
    queryset = models.ProxyNode.objects.all()


class ProxyNodeBulkDeleteView(generic.BulkDeleteView):
    queryset = models.ProxyNode.objects.all()
    table = tables.ProxyNodeTable


# ── ProxyVHost ────────────────────────────────────────────────────────────────

class ProxyVHostListView(generic.ObjectListView):
    queryset = models.ProxyVHost.objects.select_related("cluster", "ssl_certificate")
    table = tables.ProxyVHostTable
    filterset = filtersets.ProxyVHostFilterSet
    filterset_form = forms.ProxyVHostFilterForm


class ProxyVHostView(generic.ObjectView):
    queryset = models.ProxyVHost.objects.select_related("cluster", "ssl_certificate")


class ProxyVHostEditView(generic.ObjectEditView):
    queryset = models.ProxyVHost.objects.all()
    form = forms.ProxyVHostForm


class ProxyVHostDeleteView(generic.ObjectDeleteView):
    queryset = models.ProxyVHost.objects.all()


class ProxyVHostBulkDeleteView(generic.BulkDeleteView):
    queryset = models.ProxyVHost.objects.all()
    table = tables.ProxyVHostTable


# ── ProxyUpstream ─────────────────────────────────────────────────────────────

class ProxyUpstreamListView(generic.ObjectListView):
    queryset = models.ProxyUpstream.objects.select_related("cluster")
    table = tables.ProxyUpstreamTable
    filterset = filtersets.ProxyUpstreamFilterSet
    filterset_form = forms.ProxyUpstreamFilterForm


class ProxyUpstreamView(generic.ObjectView):
    queryset = models.ProxyUpstream.objects.select_related("cluster")


class ProxyUpstreamEditView(generic.ObjectEditView):
    queryset = models.ProxyUpstream.objects.all()
    form = forms.ProxyUpstreamForm


class ProxyUpstreamDeleteView(generic.ObjectDeleteView):
    queryset = models.ProxyUpstream.objects.all()


class ProxyUpstreamBulkDeleteView(generic.BulkDeleteView):
    queryset = models.ProxyUpstream.objects.all()
    table = tables.ProxyUpstreamTable


# ── ProxyUpstreamServer ───────────────────────────────────────────────────────

class ProxyUpstreamServerListView(generic.ObjectListView):
    queryset = models.ProxyUpstreamServer.objects.select_related("upstream__cluster")
    table = tables.ProxyUpstreamServerTable
    filterset = filtersets.ProxyUpstreamServerFilterSet
    filterset_form = forms.ProxyUpstreamServerFilterForm


class ProxyUpstreamServerView(generic.ObjectView):
    queryset = models.ProxyUpstreamServer.objects.select_related("upstream__cluster")


class ProxyUpstreamServerEditView(generic.ObjectEditView):
    queryset = models.ProxyUpstreamServer.objects.all()
    form = forms.ProxyUpstreamServerForm


class ProxyUpstreamServerDeleteView(generic.ObjectDeleteView):
    queryset = models.ProxyUpstreamServer.objects.all()


class ProxyUpstreamServerBulkDeleteView(generic.BulkDeleteView):
    queryset = models.ProxyUpstreamServer.objects.all()
    table = tables.ProxyUpstreamServerTable


# ── ProxySSLCertificate ───────────────────────────────────────────────────────

class ProxySSLCertificateListView(generic.ObjectListView):
    queryset = models.ProxySSLCertificate.objects.all()
    table = tables.ProxySSLCertificateTable
    filterset = filtersets.ProxySSLCertificateFilterSet
    filterset_form = forms.ProxySSLCertificateFilterForm


class ProxySSLCertificateView(generic.ObjectView):
    queryset = models.ProxySSLCertificate.objects.all()


class ProxySSLCertificateEditView(generic.ObjectEditView):
    queryset = models.ProxySSLCertificate.objects.all()
    form = forms.ProxySSLCertificateForm


class ProxySSLCertificateDeleteView(generic.ObjectDeleteView):
    queryset = models.ProxySSLCertificate.objects.all()


class ProxySSLCertificateBulkDeleteView(generic.BulkDeleteView):
    queryset = models.ProxySSLCertificate.objects.all()
    table = tables.ProxySSLCertificateTable


# ── ProxyRateLimit ────────────────────────────────────────────────────────────

class ProxyRateLimitListView(generic.ObjectListView):
    queryset = models.ProxyRateLimit.objects.all()
    table = tables.ProxyRateLimitTable
    filterset = filtersets.ProxyRateLimitFilterSet
    filterset_form = forms.ProxyRateLimitFilterForm


class ProxyRateLimitView(generic.ObjectView):
    queryset = models.ProxyRateLimit.objects.all()


class ProxyRateLimitEditView(generic.ObjectEditView):
    queryset = models.ProxyRateLimit.objects.all()
    form = forms.ProxyRateLimitForm


class ProxyRateLimitDeleteView(generic.ObjectDeleteView):
    queryset = models.ProxyRateLimit.objects.all()


class ProxyRateLimitBulkDeleteView(generic.BulkDeleteView):
    queryset = models.ProxyRateLimit.objects.all()
    table = tables.ProxyRateLimitTable


# ── ProxyLocation ─────────────────────────────────────────────────────────────

class ProxyLocationListView(generic.ObjectListView):
    queryset = models.ProxyLocation.objects.select_related(
        "vhost__cluster", "upstream", "rate_limit"
    )
    table = tables.ProxyLocationTable
    filterset = filtersets.ProxyLocationFilterSet
    filterset_form = forms.ProxyLocationFilterForm


class ProxyLocationView(generic.ObjectView):
    queryset = models.ProxyLocation.objects.select_related(
        "vhost__cluster", "upstream", "rate_limit"
    )


class ProxyLocationEditView(generic.ObjectEditView):
    queryset = models.ProxyLocation.objects.all()
    form = forms.ProxyLocationForm


class ProxyLocationDeleteView(generic.ObjectDeleteView):
    queryset = models.ProxyLocation.objects.all()


class ProxyLocationBulkDeleteView(generic.BulkDeleteView):
    queryset = models.ProxyLocation.objects.all()
    table = tables.ProxyLocationTable


# ── ProxyDeployment ───────────────────────────────────────────────────────────

class ProxyDeploymentListView(generic.ObjectListView):
    queryset = models.ProxyDeployment.objects.select_related("cluster", "initiated_by")
    table = tables.ProxyDeploymentTable
    filterset = filtersets.ProxyDeploymentFilterSet
    filterset_form = forms.ProxyDeploymentFilterForm


class ProxyDeploymentView(generic.ObjectView):
    queryset = models.ProxyDeployment.objects.select_related(
        "cluster", "initiated_by", "rpc_execution"
    )


class ProxyDeploymentEditView(generic.ObjectEditView):
    queryset = models.ProxyDeployment.objects.all()
    form = forms.ProxyDeploymentForm


class ProxyDeploymentDeleteView(generic.ObjectDeleteView):
    queryset = models.ProxyDeployment.objects.all()


class ProxyDeploymentBulkDeleteView(generic.BulkDeleteView):
    queryset = models.ProxyDeployment.objects.all()
    table = tables.ProxyDeploymentTable
