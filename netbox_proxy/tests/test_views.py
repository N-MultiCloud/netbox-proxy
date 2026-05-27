"""
UI view tests for netbox_proxy.

Exercises list, detail, create, edit, and delete views for all nine models.
Uses NetBox's ViewTestCases helpers where available; falls back to
authenticated GET checks for simpler coverage.
"""

from django.test import TestCase
from django.urls import reverse

from utilities.testing import ViewTestCases

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

def _cluster(name="view-cluster"):
    return ProxyCluster.objects.create(name=name)


def _vhost(cluster, name="view-vhost"):
    return ProxyVHost.objects.create(
        cluster=cluster, name=name, server_names="view.example.com"
    )


def _upstream(cluster, name="view-upstream"):
    return ProxyUpstream.objects.create(cluster=cluster, name=name)


# ---------------------------------------------------------------------------
# ProxyCluster
# ---------------------------------------------------------------------------

class ProxyClusterViewTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
):
    model = ProxyCluster

    @classmethod
    def setUpTestData(cls):
        ProxyCluster.objects.bulk_create([
            ProxyCluster(name="vc-1"),
            ProxyCluster(name="vc-2"),
            ProxyCluster(name="vc-3"),
        ])

        cls.form_data = {"name": "vc-new"}
        cls.csv_data = (
            "name",
            "vc-csv-1",
            "vc-csv-2",
            "vc-csv-3",
        )
        cls.bulk_edit_data = {"description": "bulk edit"}


# ---------------------------------------------------------------------------
# ProxyNode
# ---------------------------------------------------------------------------

class ProxyNodeViewTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
):
    model = ProxyNode

    @classmethod
    def setUpTestData(cls):
        cluster = _cluster("node-view-cluster")
        ProxyNode.objects.bulk_create([
            ProxyNode(cluster=cluster, name="vn-1"),
            ProxyNode(cluster=cluster, name="vn-2"),
            ProxyNode(cluster=cluster, name="vn-3"),
        ])

        cls.form_data = {"cluster": cluster.pk, "name": "vn-new"}
        cls.bulk_edit_data = {"management_ip": "10.0.9.9"}


# ---------------------------------------------------------------------------
# ProxySSLCertificate
# ---------------------------------------------------------------------------

class ProxySSLCertificateViewTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
):
    model = ProxySSLCertificate

    @classmethod
    def setUpTestData(cls):
        ProxySSLCertificate.objects.bulk_create([
            ProxySSLCertificate(name="vc-cert-1", domain="a.example.com"),
            ProxySSLCertificate(name="vc-cert-2", domain="b.example.com"),
            ProxySSLCertificate(name="vc-cert-3", domain="c.example.com"),
        ])

        cls.form_data = {"name": "vc-cert-new", "domain": "new.example.com"}
        cls.bulk_edit_data = {"auto_renew": True}


# ---------------------------------------------------------------------------
# ProxyVHost
# ---------------------------------------------------------------------------

class ProxyVHostViewTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
):
    model = ProxyVHost

    @classmethod
    def setUpTestData(cls):
        cluster = _cluster("vhost-view-cluster")
        ProxyVHost.objects.bulk_create([
            ProxyVHost(
                cluster=cluster,
                name="vvh-1",
                server_names="v1.example.com",
            ),
            ProxyVHost(
                cluster=cluster,
                name="vvh-2",
                server_names="v2.example.com",
            ),
            ProxyVHost(
                cluster=cluster,
                name="vvh-3",
                server_names="v3.example.com",
            ),
        ])

        cls.form_data = {
            "cluster": cluster.pk,
            "name": "vvh-new",
            "server_names": "new.example.com",
            "listen_port": 80,
            "listen_ssl_port": 443,
            "ssl_mode": "off",
            "is_enabled": True,
            "is_default_server": False,
        }
        cls.bulk_edit_data = {"is_enabled": False}


# ---------------------------------------------------------------------------
# ProxyUpstream
# ---------------------------------------------------------------------------

class ProxyUpstreamViewTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
):
    model = ProxyUpstream

    @classmethod
    def setUpTestData(cls):
        cluster = _cluster("upstream-view-cluster")
        ProxyUpstream.objects.bulk_create([
            ProxyUpstream(cluster=cluster, name="vus-1"),
            ProxyUpstream(cluster=cluster, name="vus-2"),
            ProxyUpstream(cluster=cluster, name="vus-3"),
        ])

        cls.form_data = {
            "cluster": cluster.pk,
            "name": "vus-new",
            "protocol": "http",
            "balance": "round_robin",
            "keepalive": 0,
            "health_check_interval": 5,
            "health_check_enabled": False,
        }
        cls.bulk_edit_data = {"health_check_enabled": True}


# ---------------------------------------------------------------------------
# ProxyUpstreamServer
# ---------------------------------------------------------------------------

class ProxyUpstreamServerViewTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
):
    model = ProxyUpstreamServer

    @classmethod
    def setUpTestData(cls):
        cluster = _cluster("server-view-cluster")
        upstream = _upstream(cluster, "server-view-upstream")
        ProxyUpstreamServer.objects.bulk_create([
            ProxyUpstreamServer(upstream=upstream, address="10.1.0.1:80"),
            ProxyUpstreamServer(upstream=upstream, address="10.1.0.2:80"),
            ProxyUpstreamServer(upstream=upstream, address="10.1.0.3:80"),
        ])

        cls.form_data = {
            "upstream": upstream.pk,
            "address": "10.1.0.99:80",
            "weight": 1,
            "max_fails": 3,
            "fail_timeout": 30,
            "enabled": True,
            "is_backup": False,
            "is_down": False,
        }
        cls.bulk_edit_data = {"weight": 2}


# ---------------------------------------------------------------------------
# ProxyRateLimit
# ---------------------------------------------------------------------------

class ProxyRateLimitViewTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
):
    model = ProxyRateLimit

    @classmethod
    def setUpTestData(cls):
        ProxyRateLimit.objects.bulk_create([
            ProxyRateLimit(name="vrl-1", rate="10r/s"),
            ProxyRateLimit(name="vrl-2", rate="20r/s"),
            ProxyRateLimit(name="vrl-3", rate="30r/s"),
        ])

        cls.form_data = {
            "name": "vrl-new",
            "rate": "5r/s",
            "burst": 5,
            "nodelay": False,
        }
        cls.bulk_edit_data = {"burst": 10}


# ---------------------------------------------------------------------------
# ProxyLocation
# ---------------------------------------------------------------------------

class ProxyLocationViewTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
):
    model = ProxyLocation

    @classmethod
    def setUpTestData(cls):
        cluster = _cluster("location-view-cluster")
        vhost = _vhost(cluster, "location-view-vhost")
        ProxyLocation.objects.bulk_create([
            ProxyLocation(vhost=vhost, path="/view/a/"),
            ProxyLocation(vhost=vhost, path="/view/b/"),
            ProxyLocation(vhost=vhost, path="/view/c/"),
        ])

        cls.form_data = {
            "vhost": vhost.pk,
            "path": "/view/new/",
            "match_type": "prefix",
            "sort_order": 100,
        }
        cls.bulk_edit_data = {"sort_order": 200}


# ---------------------------------------------------------------------------
# ProxyDeployment
# ---------------------------------------------------------------------------

class ProxyDeploymentViewTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
):
    model = ProxyDeployment

    @classmethod
    def setUpTestData(cls):
        cluster = _cluster("deploy-view-cluster")
        ProxyDeployment.objects.bulk_create([
            ProxyDeployment(
                cluster=cluster, status=DeployStatusChoices.STATUS_SUCCESS
            ),
            ProxyDeployment(
                cluster=cluster, status=DeployStatusChoices.STATUS_FAILED
            ),
            ProxyDeployment(
                cluster=cluster, status=DeployStatusChoices.STATUS_PENDING
            ),
        ])

        cls.form_data = {"cluster": cluster.pk}
        cls.bulk_edit_data = {"status": DeployStatusChoices.STATUS_PENDING}
