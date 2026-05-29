"""
Form validation tests for netbox_proxy.

Tests required fields, optional fields, and that invalid combinations are
rejected.  The DynamicModelChoiceField widgets used in most forms require a
live database, which is satisfied by the Django TestCase base class.
"""

from django.test import TestCase

from netbox_proxy.forms import (
    ProxyClusterForm,
    ProxyDeploymentForm,
    ProxyLocationForm,
    ProxyNodeForm,
    ProxyRateLimitForm,
    ProxySSLCertificateForm,
    ProxyUpstreamForm,
    ProxyUpstreamServerForm,
    ProxyVHostForm,
)
from netbox_proxy.models import (
    ProxyCluster,
    ProxySSLCertificate,
    ProxyUpstream,
    ProxyVHost,
    ProxyNode,
    ProxyRateLimit,
)


# ---------------------------------------------------------------------------
# ProxyClusterForm
# ---------------------------------------------------------------------------


class ProxyClusterFormTestCase(TestCase):
    def test_valid_minimal(self):
        form = ProxyClusterForm(data={"name": "my-cluster"})
        self.assertTrue(form.is_valid(), form.errors)

    def test_name_required(self):
        form = ProxyClusterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_name_max_length(self):
        form = ProxyClusterForm(data={"name": "x" * 256})
        self.assertFalse(form.is_valid())


# ---------------------------------------------------------------------------
# ProxyNodeForm
# ---------------------------------------------------------------------------


class ProxyNodeFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cluster = ProxyCluster.objects.create(name="node-form-cluster")

    def test_valid_minimal(self):
        form = ProxyNodeForm(data={"cluster": self.cluster.pk, "name": "node-form-1"})
        self.assertTrue(form.is_valid(), form.errors)

    def test_cluster_required(self):
        form = ProxyNodeForm(data={"name": "node-form-2"})
        self.assertFalse(form.is_valid())
        self.assertIn("cluster", form.errors)

    def test_name_required(self):
        form = ProxyNodeForm(data={"cluster": self.cluster.pk})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


# ---------------------------------------------------------------------------
# ProxySSLCertificateForm
# ---------------------------------------------------------------------------


class ProxySSLCertificateFormTestCase(TestCase):
    def test_valid_minimal(self):
        form = ProxySSLCertificateForm(
            data={"name": "cert-form-1", "domain": "cert.example.com"}
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_name_required(self):
        form = ProxySSLCertificateForm(data={"domain": "x.com"})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_domain_required(self):
        form = ProxySSLCertificateForm(data={"name": "cert-no-domain"})
        self.assertFalse(form.is_valid())
        self.assertIn("domain", form.errors)


# ---------------------------------------------------------------------------
# ProxyVHostForm
# ---------------------------------------------------------------------------


class ProxyVHostFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cluster = ProxyCluster.objects.create(name="vhost-form-cluster")
        cls.cert = ProxySSLCertificate.objects.create(
            name="vhost-form-cert", domain="vh.example.com"
        )

    def test_valid_minimal(self):
        form = ProxyVHostForm(
            data={
                "cluster": self.cluster.pk,
                "name": "vh-form-1",
                "server_names": "vh1.example.com",
                "listen_port": 80,
                "listen_ssl_port": 443,
                "ssl_mode": "off",
                "is_enabled": True,
                "is_default_server": False,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_cluster_required(self):
        form = ProxyVHostForm(
            data={
                "name": "vh-no-cluster",
                "server_names": "vh.example.com",
                "listen_port": 80,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("cluster", form.errors)

    def test_server_names_required(self):
        form = ProxyVHostForm(
            data={
                "cluster": self.cluster.pk,
                "name": "vh-no-server-names",
                "listen_port": 80,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("server_names", form.errors)

    def test_ssl_certificate_optional(self):
        form = ProxyVHostForm(
            data={
                "cluster": self.cluster.pk,
                "name": "vh-no-cert",
                "server_names": "no-cert.example.com",
                "listen_port": 80,
                "listen_ssl_port": 443,
                "ssl_mode": "off",
                "is_enabled": True,
                "is_default_server": False,
                # ssl_certificate intentionally omitted
            }
        )
        self.assertTrue(form.is_valid(), form.errors)


# ---------------------------------------------------------------------------
# ProxyUpstreamForm
# ---------------------------------------------------------------------------


class ProxyUpstreamFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cluster = ProxyCluster.objects.create(name="upstream-form-cluster")

    def test_valid_minimal(self):
        form = ProxyUpstreamForm(
            data={
                "cluster": self.cluster.pk,
                "name": "us-form-1",
                "protocol": "http",
                "balance": "round_robin",
                "keepalive": 0,
                "health_check_interval": 5,
                "health_check_enabled": False,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_cluster_required(self):
        form = ProxyUpstreamForm(data={"name": "us-no-cluster"})
        self.assertFalse(form.is_valid())
        self.assertIn("cluster", form.errors)


# ---------------------------------------------------------------------------
# ProxyUpstreamServerForm
# ---------------------------------------------------------------------------


class ProxyUpstreamServerFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cluster = ProxyCluster.objects.create(name="server-form-cluster")
        cls.upstream = ProxyUpstream.objects.create(
            cluster=cluster, name="server-form-upstream"
        )

    def test_valid_minimal(self):
        form = ProxyUpstreamServerForm(
            data={
                "upstream": self.upstream.pk,
                "address": "10.0.5.5:8080",
                "weight": 1,
                "max_fails": 3,
                "fail_timeout": 30,
                "enabled": True,
                "is_backup": False,
                "is_down": False,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_upstream_required(self):
        form = ProxyUpstreamServerForm(data={"address": "1.2.3.4:80"})
        self.assertFalse(form.is_valid())
        self.assertIn("upstream", form.errors)

    def test_address_required(self):
        form = ProxyUpstreamServerForm(data={"upstream": self.upstream.pk})
        self.assertFalse(form.is_valid())
        self.assertIn("address", form.errors)


# ---------------------------------------------------------------------------
# ProxyRateLimitForm
# ---------------------------------------------------------------------------


class ProxyRateLimitFormTestCase(TestCase):
    def test_valid_minimal(self):
        form = ProxyRateLimitForm(
            data={
                "name": "rl-form-1",
                "rate": "10r/s",
                "burst": 5,
                "nodelay": False,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_name_required(self):
        form = ProxyRateLimitForm(data={"rate": "10r/s"})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_rate_required(self):
        form = ProxyRateLimitForm(data={"name": "rl-no-rate"})
        self.assertFalse(form.is_valid())
        self.assertIn("rate", form.errors)

    def test_vhost_optional(self):
        form = ProxyRateLimitForm(
            data={
                "name": "rl-no-vhost",
                "rate": "5r/s",
                "burst": 3,
                "nodelay": False,
                # vhost intentionally omitted
            }
        )
        self.assertTrue(form.is_valid(), form.errors)


# ---------------------------------------------------------------------------
# ProxyLocationForm
# ---------------------------------------------------------------------------


class ProxyLocationFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cluster = ProxyCluster.objects.create(name="loc-form-cluster")
        cls.vhost = ProxyVHost.objects.create(
            cluster=cluster, name="loc-form-vhost", server_names="loc.example.com"
        )
        cls.upstream = ProxyUpstream.objects.create(
            cluster=cluster, name="loc-form-upstream"
        )
        cls.rate_limit = ProxyRateLimit.objects.create(name="loc-form-rl", rate="10r/s")

    def test_valid_minimal(self):
        form = ProxyLocationForm(
            data={
                "vhost": self.vhost.pk,
                "path": "/form-test/",
                "match_type": "prefix",
                "sort_order": 100,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_vhost_required(self):
        form = ProxyLocationForm(data={"path": "/no-vhost/"})
        self.assertFalse(form.is_valid())
        self.assertIn("vhost", form.errors)

    def test_path_required(self):
        form = ProxyLocationForm(data={"vhost": self.vhost.pk})
        self.assertFalse(form.is_valid())
        self.assertIn("path", form.errors)


# ---------------------------------------------------------------------------
# ProxyDeploymentForm
# ---------------------------------------------------------------------------


class ProxyDeploymentFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cluster = ProxyCluster.objects.create(name="dep-form-cluster")
        cls.node = ProxyNode.objects.create(cluster=cls.cluster, name="dep-form-node")

    def test_valid_minimal(self):
        form = ProxyDeploymentForm(data={"cluster": self.cluster.pk})
        self.assertTrue(form.is_valid(), form.errors)

    def test_cluster_required(self):
        form = ProxyDeploymentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("cluster", form.errors)

    def test_node_optional(self):
        form = ProxyDeploymentForm(
            data={"cluster": self.cluster.pk}
            # node intentionally omitted
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_node_accepted(self):
        form = ProxyDeploymentForm(
            data={"cluster": self.cluster.pk, "node": self.node.pk}
        )
        self.assertTrue(form.is_valid(), form.errors)
