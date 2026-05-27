"""
FilterSet tests for netbox_proxy.

Verifies that each FilterSet can be instantiated with query data, that
filter results are correct, and that the key filterable fields work as
expected (queryset length and object membership).
"""

from django.test import TestCase

from netbox_proxy.choices import DeployStatusChoices
from netbox_proxy.filtersets import (
    ProxyClusterFilterSet,
    ProxyDeploymentFilterSet,
    ProxyLocationFilterSet,
    ProxyNodeFilterSet,
    ProxyRateLimitFilterSet,
    ProxySSLCertificateFilterSet,
    ProxyUpstreamFilterSet,
    ProxyUpstreamServerFilterSet,
    ProxyVHostFilterSet,
)
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


class ProxyClusterFilterSetTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        ProxyCluster.objects.bulk_create([
            ProxyCluster(name="alpha-cluster", description="first"),
            ProxyCluster(name="beta-cluster", description="second"),
            ProxyCluster(name="gamma-cluster"),
        ])

    def test_filter_by_name(self):
        fs = ProxyClusterFilterSet({"name": "alpha"}, queryset=ProxyCluster.objects.all())
        self.assertEqual(fs.qs.count(), 1)
        self.assertEqual(fs.qs.first().name, "alpha-cluster")

    def test_filter_by_name_icontains(self):
        fs = ProxyClusterFilterSet({"name": "cluster"}, queryset=ProxyCluster.objects.all())
        self.assertEqual(fs.qs.count(), 3)

    def test_empty_filter(self):
        fs = ProxyClusterFilterSet({}, queryset=ProxyCluster.objects.all())
        self.assertEqual(fs.qs.count(), 3)


class ProxyNodeFilterSetTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.cluster_a = ProxyCluster.objects.create(name="fs-cluster-a")
        cls.cluster_b = ProxyCluster.objects.create(name="fs-cluster-b")
        ProxyNode.objects.bulk_create([
            ProxyNode(
                cluster=cls.cluster_a,
                name="node-x",
                management_ip="10.0.1.1",
                is_active=True,
            ),
            ProxyNode(
                cluster=cls.cluster_a,
                name="node-y",
                management_ip="10.0.1.2",
                is_active=False,
            ),
            ProxyNode(
                cluster=cls.cluster_b,
                name="node-z",
                management_ip="192.168.0.1",
                is_active=True,
            ),
        ])

    def test_filter_by_cluster_id(self):
        fs = ProxyNodeFilterSet(
            {"cluster_id": [self.cluster_a.pk]},
            queryset=ProxyNode.objects.all(),
        )
        self.assertEqual(fs.qs.count(), 2)

    def test_filter_by_is_active_true(self):
        fs = ProxyNodeFilterSet({"is_active": True}, queryset=ProxyNode.objects.all())
        self.assertEqual(fs.qs.count(), 2)

    def test_filter_by_is_active_false(self):
        fs = ProxyNodeFilterSet({"is_active": False}, queryset=ProxyNode.objects.all())
        self.assertEqual(fs.qs.count(), 1)

    def test_filter_by_management_ip(self):
        fs = ProxyNodeFilterSet(
            {"management_ip": "10.0"},
            queryset=ProxyNode.objects.all(),
        )
        self.assertEqual(fs.qs.count(), 2)


class ProxyVHostFilterSetTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.cluster = ProxyCluster.objects.create(name="vhost-fs-cluster")
        ProxyVHost.objects.bulk_create([
            ProxyVHost(
                cluster=cls.cluster,
                name="vh1",
                server_names="a.example.com",
                ssl_mode="off",
                listen_port=80,
                is_enabled=True,
            ),
            ProxyVHost(
                cluster=cls.cluster,
                name="vh2",
                server_names="b.example.com",
                ssl_mode="on",
                listen_port=443,
                is_enabled=True,
            ),
            ProxyVHost(
                cluster=cls.cluster,
                name="vh3",
                server_names="c.example.com",
                ssl_mode="strict",
                listen_port=8080,
                is_enabled=False,
            ),
        ])

    def test_filter_by_ssl_mode(self):
        fs = ProxyVHostFilterSet(
            {"ssl_mode": ["on"]},
            queryset=ProxyVHost.objects.all(),
        )
        self.assertEqual(fs.qs.count(), 1)

    def test_filter_by_is_enabled(self):
        fs = ProxyVHostFilterSet(
            {"is_enabled": True},
            queryset=ProxyVHost.objects.all(),
        )
        self.assertEqual(fs.qs.count(), 2)

    def test_filter_by_cluster_id(self):
        other = ProxyCluster.objects.create(name="other-vhost-cluster")
        fs = ProxyVHostFilterSet(
            {"cluster_id": [other.pk]},
            queryset=ProxyVHost.objects.all(),
        )
        self.assertEqual(fs.qs.count(), 0)


class ProxyUpstreamFilterSetTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.cluster = ProxyCluster.objects.create(name="upstream-fs-cluster")
        ProxyUpstream.objects.bulk_create([
            ProxyUpstream(
                cluster=cls.cluster,
                name="up1",
                protocol="http",
                balance="round_robin",
                health_check_enabled=False,
            ),
            ProxyUpstream(
                cluster=cls.cluster,
                name="up2",
                protocol="https",
                balance="least_conn",
                health_check_enabled=True,
            ),
        ])

    def test_filter_by_protocol(self):
        fs = ProxyUpstreamFilterSet(
            {"protocol": ["http"]},
            queryset=ProxyUpstream.objects.all(),
        )
        self.assertEqual(fs.qs.count(), 1)
        self.assertEqual(fs.qs.first().name, "up1")

    def test_filter_by_health_check_enabled(self):
        fs = ProxyUpstreamFilterSet(
            {"health_check_enabled": True},
            queryset=ProxyUpstream.objects.all(),
        )
        self.assertEqual(fs.qs.count(), 1)

    def test_filter_by_balance(self):
        fs = ProxyUpstreamFilterSet(
            {"balance": ["least_conn"]},
            queryset=ProxyUpstream.objects.all(),
        )
        self.assertEqual(fs.qs.count(), 1)


class ProxyUpstreamServerFilterSetTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cluster = ProxyCluster.objects.create(name="srv-fs-cluster")
        cls.upstream = ProxyUpstream.objects.create(cluster=cluster, name="srv-upstream")
        ProxyUpstreamServer.objects.bulk_create([
            ProxyUpstreamServer(
                upstream=cls.upstream,
                address="1.1.1.1:80",
                enabled=True,
                is_backup=False,
                is_down=False,
            ),
            ProxyUpstreamServer(
                upstream=cls.upstream,
                address="2.2.2.2:80",
                enabled=False,
                is_backup=True,
                is_down=False,
            ),
        ])

    def test_filter_by_upstream_id(self):
        fs = ProxyUpstreamServerFilterSet(
            {"upstream_id": [self.upstream.pk]},
            queryset=ProxyUpstreamServer.objects.all(),
        )
        self.assertEqual(fs.qs.count(), 2)

    def test_filter_by_enabled(self):
        fs = ProxyUpstreamServerFilterSet(
            {"enabled": True},
            queryset=ProxyUpstreamServer.objects.all(),
        )
        self.assertEqual(fs.qs.count(), 1)

    def test_filter_by_is_backup(self):
        fs = ProxyUpstreamServerFilterSet(
            {"is_backup": True},
            queryset=ProxyUpstreamServer.objects.all(),
        )
        self.assertEqual(fs.qs.count(), 1)


class ProxySSLCertificateFilterSetTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        ProxySSLCertificate.objects.bulk_create([
            ProxySSLCertificate(
                name="cert-manual",
                provider="manual",
                domain="manual.example.com",
                auto_renew=False,
            ),
            ProxySSLCertificate(
                name="cert-le",
                provider="letsencrypt",
                domain="le.example.com",
                auto_renew=True,
            ),
        ])

    def test_filter_by_provider(self):
        fs = ProxySSLCertificateFilterSet(
            {"provider": ["letsencrypt"]},
            queryset=ProxySSLCertificate.objects.all(),
        )
        self.assertEqual(fs.qs.count(), 1)

    def test_filter_by_auto_renew(self):
        fs = ProxySSLCertificateFilterSet(
            {"auto_renew": True},
            queryset=ProxySSLCertificate.objects.all(),
        )
        self.assertEqual(fs.qs.count(), 1)

    def test_filter_by_domain(self):
        fs = ProxySSLCertificateFilterSet(
            {"domain": "le."},
            queryset=ProxySSLCertificate.objects.all(),
        )
        self.assertEqual(fs.qs.count(), 1)


class ProxyRateLimitFilterSetTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.cluster = ProxyCluster.objects.create(name="rl-fs-cluster")
        cls.vhost = ProxyVHost.objects.create(
            cluster=cls.cluster, name="rl-vhost", server_names="rl.example.com"
        )
        ProxyRateLimit.objects.bulk_create([
            ProxyRateLimit(name="global-rl", rate="10r/s"),
            ProxyRateLimit(name="scoped-rl", vhost=cls.vhost, rate="5r/s"),
        ])

    def test_filter_by_name(self):
        fs = ProxyRateLimitFilterSet(
            {"name": "global"},
            queryset=ProxyRateLimit.objects.all(),
        )
        self.assertEqual(fs.qs.count(), 1)

    def test_filter_by_vhost_id(self):
        fs = ProxyRateLimitFilterSet(
            {"vhost_id": [self.vhost.pk]},
            queryset=ProxyRateLimit.objects.all(),
        )
        self.assertEqual(fs.qs.count(), 1)


class ProxyLocationFilterSetTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cluster = ProxyCluster.objects.create(name="loc-fs-cluster")
        cls.vhost = ProxyVHost.objects.create(
            cluster=cluster, name="loc-vhost", server_names="loc.example.com"
        )
        cls.upstream = ProxyUpstream.objects.create(cluster=cluster, name="loc-upstream")
        ProxyLocation.objects.bulk_create([
            ProxyLocation(
                vhost=cls.vhost,
                path="/api/",
                match_type="prefix",
                upstream=cls.upstream,
            ),
            ProxyLocation(
                vhost=cls.vhost,
                path="/static/",
                match_type="exact",
            ),
        ])

    def test_filter_by_vhost_id(self):
        fs = ProxyLocationFilterSet(
            {"vhost_id": [self.vhost.pk]},
            queryset=ProxyLocation.objects.all(),
        )
        self.assertEqual(fs.qs.count(), 2)

    def test_filter_by_match_type(self):
        fs = ProxyLocationFilterSet(
            {"match_type": ["exact"]},
            queryset=ProxyLocation.objects.all(),
        )
        self.assertEqual(fs.qs.count(), 1)

    def test_filter_by_upstream_id(self):
        fs = ProxyLocationFilterSet(
            {"upstream_id": [self.upstream.pk]},
            queryset=ProxyLocation.objects.all(),
        )
        self.assertEqual(fs.qs.count(), 1)


class ProxyDeploymentFilterSetTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.cluster = ProxyCluster.objects.create(name="dep-fs-cluster")
        cls.node = ProxyNode.objects.create(cluster=cls.cluster, name="dep-fs-node")
        ProxyDeployment.objects.bulk_create([
            ProxyDeployment(
                cluster=cls.cluster,
                node=cls.node,
                status=DeployStatusChoices.STATUS_SUCCESS,
            ),
            ProxyDeployment(
                cluster=cls.cluster,
                status=DeployStatusChoices.STATUS_FAILED,
            ),
            ProxyDeployment(
                cluster=cls.cluster,
                status=DeployStatusChoices.STATUS_PENDING,
            ),
        ])

    def test_filter_by_status_success(self):
        fs = ProxyDeploymentFilterSet(
            {"status": ["success"]},
            queryset=ProxyDeployment.objects.all(),
        )
        self.assertEqual(fs.qs.count(), 1)

    def test_filter_by_status_multiple(self):
        fs = ProxyDeploymentFilterSet(
            {"status": ["success", "failed"]},
            queryset=ProxyDeployment.objects.all(),
        )
        self.assertEqual(fs.qs.count(), 2)

    def test_filter_by_cluster_id(self):
        other = ProxyCluster.objects.create(name="other-dep-cluster")
        fs = ProxyDeploymentFilterSet(
            {"cluster_id": [other.pk]},
            queryset=ProxyDeployment.objects.all(),
        )
        self.assertEqual(fs.qs.count(), 0)

    def test_filter_by_node_id(self):
        fs = ProxyDeploymentFilterSet(
            {"node_id": [self.node.pk]},
            queryset=ProxyDeployment.objects.all(),
        )
        self.assertEqual(fs.qs.count(), 1)

    def test_status_rolled_back_accepted(self):
        """Verify 'rolled_back' is a valid filter value (bugfix regression)."""
        dep = ProxyDeployment.objects.create(
            cluster=self.cluster,
            status=DeployStatusChoices.STATUS_ROLLED_BACK,
        )
        fs = ProxyDeploymentFilterSet(
            {"status": ["rolled_back"]},
            queryset=ProxyDeployment.objects.all(),
        )
        pks = list(fs.qs.values_list("pk", flat=True))
        self.assertIn(dep.pk, pks)

    def test_invalid_legacy_status_not_in_choices(self):
        """The old 'running'/'rolledback'/'skipped'/'cancelled'/'partial'
        values were never valid for DeployStatusChoices and should not appear
        in the corrected filterset choices."""
        from netbox_proxy.filtersets import ProxyDeploymentFilterSet as PDFS
        valid_values = {c[0] for c in PDFS.declared_filters["status"].field.choices}
        invalid = {"running", "rolledback", "skipped", "cancelled", "partial"}
        overlap = valid_values & invalid
        self.assertFalse(
            overlap,
            msg=f"Stale status values found in filterset choices: {overlap}",
        )
