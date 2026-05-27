"""
Model tests for netbox_proxy.

Covers: __str__, unique_together / unique field constraints, FK cascade and
SET_NULL behaviours, GenericForeignKey wiring, and a sanity-check that the
0002 seed migration data is structurally correct (importlib is required because
module names that begin with a digit cannot be imported with the normal
``from x.0y import z`` syntax).
"""

import importlib

from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, transaction
from django.test import TestCase

from dcim.models import Site

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
# Shared fixtures
# ---------------------------------------------------------------------------

def _cluster(name="test-cluster"):
    return ProxyCluster.objects.create(name=name)


def _ssl_cert(name="test-cert"):
    return ProxySSLCertificate.objects.create(name=name, domain="example.com")


def _vhost(cluster, name="vhost1"):
    return ProxyVHost.objects.create(
        cluster=cluster,
        name=name,
        server_names="example.com",
    )


def _upstream(cluster, name="upstream1"):
    return ProxyUpstream.objects.create(cluster=cluster, name=name)


# ---------------------------------------------------------------------------
# ProxyCluster
# ---------------------------------------------------------------------------

class ProxyClusterTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.cluster = _cluster()

    def test_str(self):
        self.assertEqual(str(self.cluster), "test-cluster")

    def test_unique_name(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ProxyCluster.objects.create(name="test-cluster")

    def test_get_absolute_url(self):
        url = self.cluster.get_absolute_url()
        self.assertIn(str(self.cluster.pk), url)


# ---------------------------------------------------------------------------
# ProxyNode
# ---------------------------------------------------------------------------

class ProxyNodeTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.cluster = _cluster("node-cluster")
        cls.node = ProxyNode.objects.create(
            cluster=cls.cluster,
            name="node-alpha",
            management_ip="10.0.0.1",
        )

    def test_str(self):
        self.assertEqual(str(self.node), "node-cluster / node-alpha")

    def test_unique_together_cluster_name(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ProxyNode.objects.create(cluster=self.cluster, name="node-alpha")

    def test_duplicate_name_different_cluster_allowed(self):
        other = _cluster("other-cluster")
        node2 = ProxyNode.objects.create(cluster=other, name="node-alpha")
        self.assertIsNotNone(node2.pk)

    def test_cascade_delete_with_cluster(self):
        cluster = _cluster("cascade-cluster")
        ProxyNode.objects.create(cluster=cluster, name="doomed-node")
        cluster.delete()
        self.assertFalse(ProxyNode.objects.filter(cluster=cluster).exists())

    def test_generic_fk_assignment(self):
        site = Site.objects.create(name="CI Site", slug="ci-site")
        ct = ContentType.objects.get_for_model(Site)
        node = ProxyNode.objects.create(
            cluster=self.cluster,
            name="gfk-node",
            assigned_object_type=ct,
            assigned_object_id=site.pk,
        )
        # Reload from DB to verify round-trip
        node.refresh_from_db()
        self.assertEqual(node.assigned_object_type, ct)
        self.assertEqual(node.assigned_object_id, site.pk)

    def test_gfk_nullable(self):
        node = ProxyNode.objects.create(cluster=self.cluster, name="no-gfk-node")
        self.assertIsNone(node.assigned_object_type)
        self.assertIsNone(node.assigned_object_id)

    def test_get_absolute_url(self):
        url = self.node.get_absolute_url()
        self.assertIn(str(self.node.pk), url)


# ---------------------------------------------------------------------------
# ProxySSLCertificate
# ---------------------------------------------------------------------------

class ProxySSLCertificateTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.cert = _ssl_cert("wildcard-cert")

    def test_str(self):
        self.assertEqual(str(self.cert), "wildcard-cert")

    def test_unique_name(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ProxySSLCertificate.objects.create(
                    name="wildcard-cert", domain="other.com"
                )

    def test_get_absolute_url(self):
        url = self.cert.get_absolute_url()
        self.assertIn(str(self.cert.pk), url)


# ---------------------------------------------------------------------------
# ProxyVHost
# ---------------------------------------------------------------------------

class ProxyVHostTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.cluster = _cluster("vhost-cluster")
        cls.cert = _ssl_cert("vhost-cert")
        cls.vhost = _vhost(cls.cluster, "main-vhost")

    def test_str(self):
        self.assertEqual(str(self.vhost), "vhost-cluster / main-vhost")

    def test_unique_together_cluster_name(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ProxyVHost.objects.create(
                    cluster=self.cluster,
                    name="main-vhost",
                    server_names="example.com",
                )

    def test_ssl_cert_set_null_on_delete(self):
        cert = ProxySSLCertificate.objects.create(name="temp-cert", domain="x.com")
        vh = ProxyVHost.objects.create(
            cluster=self.cluster,
            name="ssl-vhost",
            server_names="x.com",
            ssl_certificate=cert,
        )
        cert.delete()
        vh.refresh_from_db()
        self.assertIsNone(vh.ssl_certificate)

    def test_cascade_delete_with_cluster(self):
        cluster = _cluster("vh-cascade")
        _vhost(cluster, "ephemeral")
        cluster.delete()
        self.assertFalse(ProxyVHost.objects.filter(cluster=cluster).exists())

    def test_get_absolute_url(self):
        url = self.vhost.get_absolute_url()
        self.assertIn(str(self.vhost.pk), url)


# ---------------------------------------------------------------------------
# ProxyUpstream
# ---------------------------------------------------------------------------

class ProxyUpstreamTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.cluster = _cluster("upstream-cluster")
        cls.upstream = _upstream(cls.cluster, "backend-pool")

    def test_str(self):
        self.assertEqual(str(self.upstream), "upstream-cluster / backend-pool")

    def test_unique_together_cluster_name(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ProxyUpstream.objects.create(cluster=self.cluster, name="backend-pool")

    def test_get_absolute_url(self):
        url = self.upstream.get_absolute_url()
        self.assertIn(str(self.upstream.pk), url)


# ---------------------------------------------------------------------------
# ProxyUpstreamServer
# ---------------------------------------------------------------------------

class ProxyUpstreamServerTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.cluster = _cluster("server-cluster")
        cls.upstream = _upstream(cls.cluster, "app-upstream")
        cls.server = ProxyUpstreamServer.objects.create(
            upstream=cls.upstream, address="10.0.1.10:8080"
        )

    def test_str(self):
        self.assertIn("app-upstream", str(self.server))
        self.assertIn("10.0.1.10:8080", str(self.server))

    def test_unique_together_upstream_address(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ProxyUpstreamServer.objects.create(
                    upstream=self.upstream, address="10.0.1.10:8080"
                )

    def test_cascade_delete_with_upstream(self):
        upstream = _upstream(self.cluster, "doomed-upstream")
        ProxyUpstreamServer.objects.create(upstream=upstream, address="1.2.3.4:80")
        upstream.delete()
        self.assertFalse(ProxyUpstreamServer.objects.filter(upstream=upstream).exists())

    def test_get_absolute_url(self):
        url = self.server.get_absolute_url()
        self.assertIn(str(self.server.pk), url)


# ---------------------------------------------------------------------------
# ProxyRateLimit
# ---------------------------------------------------------------------------

class ProxyRateLimitTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.cluster = _cluster("rl-cluster")
        cls.vhost = _vhost(cls.cluster, "rl-vhost")
        cls.rl = ProxyRateLimit.objects.create(
            name="global-rl",
            rate="10r/s",
        )

    def test_str(self):
        self.assertEqual(str(self.rl), "global-rl")

    def test_unique_name(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ProxyRateLimit.objects.create(name="global-rl", rate="5r/s")

    def test_vhost_set_null_on_delete(self):
        vhost = _vhost(self.cluster, "rl-vhost-2")
        rl = ProxyRateLimit.objects.create(
            name="scoped-rl",
            vhost=vhost,
            rate="5r/m",
        )
        vhost.delete()
        rl.refresh_from_db()
        self.assertIsNone(rl.vhost)

    def test_get_absolute_url(self):
        url = self.rl.get_absolute_url()
        self.assertIn(str(self.rl.pk), url)


# ---------------------------------------------------------------------------
# ProxyLocation
# ---------------------------------------------------------------------------

class ProxyLocationTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.cluster = _cluster("loc-cluster")
        cls.vhost = _vhost(cls.cluster, "loc-vhost")
        cls.upstream = _upstream(cls.cluster, "loc-upstream")
        cls.location = ProxyLocation.objects.create(
            vhost=cls.vhost,
            path="/api/",
        )

    def test_str(self):
        self.assertIn("/api/", str(self.location))

    def test_unique_together_vhost_path(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ProxyLocation.objects.create(vhost=self.vhost, path="/api/")

    def test_upstream_set_null_on_delete(self):
        upstream = _upstream(self.cluster, "temp-upstream")
        loc = ProxyLocation.objects.create(
            vhost=self.vhost, path="/proxy/", upstream=upstream
        )
        upstream.delete()
        loc.refresh_from_db()
        self.assertIsNone(loc.upstream)

    def test_cascade_delete_with_vhost(self):
        vhost = _vhost(self.cluster, "cascade-vhost")
        ProxyLocation.objects.create(vhost=vhost, path="/delete-me/")
        vhost.delete()
        self.assertFalse(ProxyLocation.objects.filter(vhost=vhost).exists())

    def test_get_absolute_url(self):
        url = self.location.get_absolute_url()
        self.assertIn(str(self.location.pk), url)


# ---------------------------------------------------------------------------
# ProxyDeployment
# ---------------------------------------------------------------------------

class ProxyDeploymentTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.cluster = _cluster("deploy-cluster")
        cls.node = ProxyNode.objects.create(cluster=cls.cluster, name="deploy-node")
        cls.deployment = ProxyDeployment.objects.create(cluster=cls.cluster)

    def test_str_contains_cluster(self):
        self.assertIn("deploy-cluster", str(self.deployment))

    def test_default_status_is_pending(self):
        self.assertEqual(self.deployment.status, DeployStatusChoices.STATUS_PENDING)

    def test_node_set_null_on_delete(self):
        node = ProxyNode.objects.create(cluster=self.cluster, name="dep-node-2")
        dep = ProxyDeployment.objects.create(cluster=self.cluster, node=node)
        node.delete()
        dep.refresh_from_db()
        self.assertIsNone(dep.node)

    def test_cascade_delete_with_cluster(self):
        cluster = _cluster("dep-cascade")
        ProxyDeployment.objects.create(cluster=cluster)
        cluster.delete()
        self.assertFalse(ProxyDeployment.objects.filter(cluster=cluster).exists())

    def test_get_absolute_url(self):
        url = self.deployment.get_absolute_url()
        self.assertIn(str(self.deployment.pk), url)


# ---------------------------------------------------------------------------
# Seed migration data integrity
# ---------------------------------------------------------------------------

class SeedMigrationDataTestCase(TestCase):
    """
    Load PROXY_RPC_PROCEDURES from the 0002 seed migration via importlib
    (cannot use a direct from-import because the module name starts with a
    digit).  Verify structural correctness without touching the database.
    """

    def _load_procedures(self):
        mod = importlib.import_module(
            "netbox_proxy.migrations.0002_seed_rpc_procedures"
        )
        return mod.PROXY_RPC_PROCEDURES

    def test_procedures_loaded(self):
        procs = self._load_procedures()
        self.assertIsInstance(procs, (list, tuple))
        self.assertGreater(len(procs), 0)

    def test_required_keys_present(self):
        required = {
            "name",
            "handler_id",
            "target_models",
            "effect",
            "timeout_seconds",
            "approval_required",
            "params_schema",
            "result_schema",
        }
        for proc in self._load_procedures():
            missing = required - set(proc.keys())
            self.assertFalse(
                missing,
                msg=f"Procedure {proc.get('name')!r} is missing keys: {missing}",
            )

    def test_effect_values_valid(self):
        valid_effects = {"read", "write"}
        for proc in self._load_procedures():
            self.assertIn(
                proc["effect"],
                valid_effects,
                msg=f"Procedure {proc['name']!r} has invalid effect {proc['effect']!r}",
            )

    def test_timeout_seconds_positive(self):
        for proc in self._load_procedures():
            self.assertGreater(
                proc["timeout_seconds"],
                0,
                msg=f"Procedure {proc['name']!r} has non-positive timeout",
            )

    def test_params_schema_is_dict(self):
        for proc in self._load_procedures():
            self.assertIsInstance(
                proc["params_schema"],
                dict,
                msg=f"Procedure {proc['name']!r} params_schema is not a dict",
            )

    def test_result_schema_is_dict(self):
        for proc in self._load_procedures():
            self.assertIsInstance(
                proc["result_schema"],
                dict,
                msg=f"Procedure {proc['name']!r} result_schema is not a dict",
            )

    def test_known_nginx_procedures_present(self):
        procs = self._load_procedures()
        names = {p["name"] for p in procs}
        expected = {
            "service.nginx.1.config_test",
            "service.nginx.1.config_deploy",
            "service.nginx.1.reload",
            "service.nginx.1.rollback",
        }
        self.assertEqual(names, expected)

    def test_target_models_non_empty_list(self):
        for proc in self._load_procedures():
            self.assertIsInstance(proc["target_models"], list)
            self.assertGreater(
                len(proc["target_models"]),
                0,
                msg=f"Procedure {proc['name']!r} has empty target_models",
            )
