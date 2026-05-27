from netbox.api.viewsets import NetBoxModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from netbox_proxy import filtersets, models

from .serializers import (
    ProxyClusterSerializer,
    ProxyDeploymentSerializer,
    ProxyLocationSerializer,
    ProxyNodeSerializer,
    ProxyRateLimitSerializer,
    ProxySSLCertificateSerializer,
    ProxyUpstreamSerializer,
    ProxyUpstreamServerSerializer,
    ProxyVHostSerializer,
)


class ProxyClusterViewSet(NetBoxModelViewSet):
    queryset = models.ProxyCluster.objects.prefetch_related("tags")
    serializer_class = ProxyClusterSerializer
    filterset_class = filtersets.ProxyClusterFilterSet

    @action(detail=True, methods=["get"], url_path="nodes")
    def nodes(self, request, pk=None):
        cluster = self.get_object()
        qs = models.ProxyNode.objects.filter(cluster=cluster)
        serializer = ProxyNodeSerializer(qs, many=True, context={"request": request})
        return Response(serializer.data)


class ProxyNodeViewSet(NetBoxModelViewSet):
    queryset = models.ProxyNode.objects.select_related("cluster").prefetch_related("tags")
    serializer_class = ProxyNodeSerializer
    filterset_class = filtersets.ProxyNodeFilterSet


class ProxyVHostViewSet(NetBoxModelViewSet):
    queryset = models.ProxyVHost.objects.select_related(
        "cluster", "ssl_certificate"
    ).prefetch_related("tags")
    serializer_class = ProxyVHostSerializer
    filterset_class = filtersets.ProxyVHostFilterSet


class ProxyUpstreamViewSet(NetBoxModelViewSet):
    queryset = models.ProxyUpstream.objects.select_related("cluster").prefetch_related("tags")
    serializer_class = ProxyUpstreamSerializer
    filterset_class = filtersets.ProxyUpstreamFilterSet


class ProxyUpstreamServerViewSet(NetBoxModelViewSet):
    queryset = models.ProxyUpstreamServer.objects.select_related(
        "upstream__cluster"
    ).prefetch_related("tags")
    serializer_class = ProxyUpstreamServerSerializer
    filterset_class = filtersets.ProxyUpstreamServerFilterSet


class ProxySSLCertificateViewSet(NetBoxModelViewSet):
    queryset = models.ProxySSLCertificate.objects.prefetch_related("tags")
    serializer_class = ProxySSLCertificateSerializer
    filterset_class = filtersets.ProxySSLCertificateFilterSet


class ProxyRateLimitViewSet(NetBoxModelViewSet):
    queryset = models.ProxyRateLimit.objects.prefetch_related("tags")
    serializer_class = ProxyRateLimitSerializer
    filterset_class = filtersets.ProxyRateLimitFilterSet


class ProxyLocationViewSet(NetBoxModelViewSet):
    queryset = models.ProxyLocation.objects.select_related(
        "vhost__cluster", "upstream", "rate_limit"
    ).prefetch_related("tags")
    serializer_class = ProxyLocationSerializer
    filterset_class = filtersets.ProxyLocationFilterSet


class ProxyDeploymentViewSet(NetBoxModelViewSet):
    queryset = models.ProxyDeployment.objects.select_related(
        "cluster", "node", "initiated_by", "rpc_execution"
    ).prefetch_related("tags")
    serializer_class = ProxyDeploymentSerializer
    filterset_class = filtersets.ProxyDeploymentFilterSet

    @action(detail=True, methods=["get"], url_path="config")
    def config_snapshot(self, request, pk=None):
        deployment = self.get_object()
        return Response({"config_snapshot": deployment.config_snapshot})
