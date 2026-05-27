"""
REST API tests for netbox_proxy.

Uses NetBox's APIViewTestCases mixins (GetObjectViewTestCase,
ListObjectsViewTestCase, CreateObjectViewTestCase, UpdateObjectViewTestCase,
DeleteObjectViewTestCase, GraphQLTestCase) to exercise the full DRF surface
for all nine models.
"""

from utilities.testing import APIViewTestCases

from netbox_proxy.choices import DeployStatusChoices
from netbox_proxy.models import (
    ProxyCluster,
    ProxyDeployment,
    ProxyLocation,
    ProxyNode,
    ProxyRateLimit,
    ProxySSLCertificate,
    ProxyUpstream,
    ProxyUpstreamServer,
    ProxyVHost,
)


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _cluster(name="api-cluster"):
    return ProxyCluster.objects.create(name=name)


def _ssl_cert(name="api-cert"):
    return ProxySSLCertificate.objects.create(name=name, domain="example.com")


def _vhost(cluster, name="api-vhost"):
    return ProxyVHost.objects.create(
        cluster=cluster, name=name, server_names="api.example.com"
    )


def _upstream(cluster, name="api-upstream"):
    return ProxyUpstream.objects.create(cluster=cluster, name=name)


# ---------------------------------------------------------------------------
# ProxyCluster
# ---------------------------------------------------------------------------

class ProxyClusterAPITestCase(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    model = ProxyCluster
    view_namespace = "plugins-api:netbox_proxy"
    brief_fields = ["display", "id", "name", "url"]

    @classmethod
    def setUpTestData(cls):
        ProxyCluster.objects.bulk_create([
            ProxyCluster(name="api-cluster-1"),
            ProxyCluster(name="api-cluster-2"),
            ProxyCluster(name="api-cluster-3"),
        ])

        cls.create_data = [
            {"name": "new-cluster-a"},
            {"name": "new-cluster-b"},
            {"name": "new-cluster-c"},
        ]
        cls.bulk_update_data = {"description": "bulk updated"}


# ---------------------------------------------------------------------------
# ProxyNode
# ---------------------------------------------------------------------------

class ProxyNodeAPITestCase(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    model = ProxyNode
    view_namespace = "plugins-api:netbox_proxy"
    brief_fields = ["display", "id", "name", "url"]

    @classmethod
    def setUpTestData(cls):
        cluster = _cluster("node-api-cluster")
        ProxyNode.objects.bulk_create([
            ProxyNode(cluster=cluster, name="api-node-1"),
            ProxyNode(cluster=cluster, name="api-node-2"),
            ProxyNode(cluster=cluster, name="api-node-3"),
        ])

        cls.create_data = [
            {"cluster": {"id": cluster.pk}, "name": "new-node-a"},
            {"cluster": {"id": cluster.pk}, "name": "new-node-b"},
            {"cluster": {"id": cluster.pk}, "name": "new-node-c"},
        ]
        cls.bulk_update_data = {"management_ip": "192.168.1.1"}


# ---------------------------------------------------------------------------
# ProxySSLCertificate
# ---------------------------------------------------------------------------

class ProxySSLCertificateAPITestCase(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    model = ProxySSLCertificate
    view_namespace = "plugins-api:netbox_proxy"
    brief_fields = ["display", "id", "name", "url"]

    @classmethod
    def setUpTestData(cls):
        ProxySSLCertificate.objects.bulk_create([
            ProxySSLCertificate(name="api-cert-1", domain="a.example.com"),
            ProxySSLCertificate(name="api-cert-2", domain="b.example.com"),
            ProxySSLCertificate(name="api-cert-3", domain="c.example.com"),
        ])

        cls.create_data = [
            {"name": "new-cert-a", "domain": "new-a.example.com"},
            {"name": "new-cert-b", "domain": "new-b.example.com"},
            {"name": "new-cert-c", "domain": "new-c.example.com"},
        ]
        cls.bulk_update_data = {"auto_renew": True}


# ---------------------------------------------------------------------------
# ProxyVHost
# ---------------------------------------------------------------------------

class ProxyVHostAPITestCase(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    model = ProxyVHost
    view_namespace = "plugins-api:netbox_proxy"
    brief_fields = ["display", "id", "name", "url"]

    @classmethod
    def setUpTestData(cls):
        cluster = _cluster("vhost-api-cluster")
        ProxyVHost.objects.bulk_create([
            ProxyVHost(
                cluster=cluster, name="api-vhost-1", server_names="v1.example.com"
            ),
            ProxyVHost(
                cluster=cluster, name="api-vhost-2", server_names="v2.example.com"
            ),
            ProxyVHost(
                cluster=cluster, name="api-vhost-3", server_names="v3.example.com"
            ),
        ])

        cls.create_data = [
            {
                "cluster": {"id": cluster.pk},
                "name": "new-vhost-a",
                "server_names": "new-a.example.com",
            },
            {
                "cluster": {"id": cluster.pk},
                "name": "new-vhost-b",
                "server_names": "new-b.example.com",
            },
            {
                "cluster": {"id": cluster.pk},
                "name": "new-vhost-c",
                "server_names": "new-c.example.com",
            },
        ]
        cls.bulk_update_data = {"is_enabled": False}


# ---------------------------------------------------------------------------
# ProxyUpstream
# ---------------------------------------------------------------------------

class ProxyUpstreamAPITestCase(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    model = ProxyUpstream
    view_namespace = "plugins-api:netbox_proxy"
    brief_fields = ["display", "id", "name", "url"]

    @classmethod
    def setUpTestData(cls):
        cluster = _cluster("upstream-api-cluster")
        ProxyUpstream.objects.bulk_create([
            ProxyUpstream(cluster=cluster, name="api-upstream-1"),
            ProxyUpstream(cluster=cluster, name="api-upstream-2"),
            ProxyUpstream(cluster=cluster, name="api-upstream-3"),
        ])

        cls.create_data = [
            {"cluster": {"id": cluster.pk}, "name": "new-upstream-a"},
            {"cluster": {"id": cluster.pk}, "name": "new-upstream-b"},
            {"cluster": {"id": cluster.pk}, "name": "new-upstream-c"},
        ]
        cls.bulk_update_data = {"health_check_enabled": True}


# ---------------------------------------------------------------------------
# ProxyUpstreamServer
# ---------------------------------------------------------------------------

class ProxyUpstreamServerAPITestCase(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    model = ProxyUpstreamServer
    view_namespace = "plugins-api:netbox_proxy"
    brief_fields = ["display", "id", "url"]

    @classmethod
    def setUpTestData(cls):
        cluster = _cluster("server-api-cluster")
        upstream = _upstream(cluster, "server-api-upstream")
        ProxyUpstreamServer.objects.bulk_create([
            ProxyUpstreamServer(upstream=upstream, address="10.0.0.1:8080"),
            ProxyUpstreamServer(upstream=upstream, address="10.0.0.2:8080"),
            ProxyUpstreamServer(upstream=upstream, address="10.0.0.3:8080"),
        ])

        cls.create_data = [
            {"upstream": {"id": upstream.pk}, "address": "10.0.0.10:8080"},
            {"upstream": {"id": upstream.pk}, "address": "10.0.0.11:8080"},
            {"upstream": {"id": upstream.pk}, "address": "10.0.0.12:8080"},
        ]
        cls.bulk_update_data = {"weight": 5}


# ---------------------------------------------------------------------------
# ProxyRateLimit
# ---------------------------------------------------------------------------

class ProxyRateLimitAPITestCase(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    model = ProxyRateLimit
    view_namespace = "plugins-api:netbox_proxy"
    brief_fields = ["display", "id", "name", "url"]

    @classmethod
    def setUpTestData(cls):
        ProxyRateLimit.objects.bulk_create([
            ProxyRateLimit(name="api-rl-1", rate="10r/s"),
            ProxyRateLimit(name="api-rl-2", rate="20r/s"),
            ProxyRateLimit(name="api-rl-3", rate="30r/s"),
        ])

        cls.create_data = [
            {"name": "new-rl-a", "rate": "5r/s"},
            {"name": "new-rl-b", "rate": "10r/s"},
            {"name": "new-rl-c", "rate": "15r/s"},
        ]
        cls.bulk_update_data = {"burst": 10}


# ---------------------------------------------------------------------------
# ProxyLocation
# ---------------------------------------------------------------------------

class ProxyLocationAPITestCase(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    model = ProxyLocation
    view_namespace = "plugins-api:netbox_proxy"
    brief_fields = ["display", "id", "url"]

    @classmethod
    def setUpTestData(cls):
        cluster = _cluster("location-api-cluster")
        vhost = _vhost(cluster, "location-api-vhost")
        ProxyLocation.objects.bulk_create([
            ProxyLocation(vhost=vhost, path="/api/v1/"),
            ProxyLocation(vhost=vhost, path="/api/v2/"),
            ProxyLocation(vhost=vhost, path="/api/v3/"),
        ])

        cls.create_data = [
            {"vhost": {"id": vhost.pk}, "path": "/new/a/"},
            {"vhost": {"id": vhost.pk}, "path": "/new/b/"},
            {"vhost": {"id": vhost.pk}, "path": "/new/c/"},
        ]
        cls.bulk_update_data = {"sort_order": 200}


# ---------------------------------------------------------------------------
# ProxyDeployment
# ---------------------------------------------------------------------------

class ProxyDeploymentAPITestCase(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    model = ProxyDeployment
    view_namespace = "plugins-api:netbox_proxy"
    brief_fields = ["display", "id", "url"]

    @classmethod
    def setUpTestData(cls):
        cluster = _cluster("deploy-api-cluster")
        ProxyDeployment.objects.bulk_create([
            ProxyDeployment(cluster=cluster, status=DeployStatusChoices.STATUS_SUCCESS),
            ProxyDeployment(cluster=cluster, status=DeployStatusChoices.STATUS_FAILED),
            ProxyDeployment(cluster=cluster, status=DeployStatusChoices.STATUS_PENDING),
        ])

        cls.create_data = [
            {"cluster": {"id": cluster.pk}},
            {"cluster": {"id": cluster.pk}},
            {"cluster": {"id": cluster.pk}},
        ]
        cls.bulk_update_data = {"status": DeployStatusChoices.STATUS_PENDING}
