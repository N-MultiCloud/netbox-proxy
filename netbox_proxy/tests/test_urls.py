"""URL contract tests for netbox-proxy UI routes."""

from django.test import TestCase
from django.urls import reverse


MODEL_URL_NAMES = (
    "proxycluster",
    "proxynode",
    "proxyvhost",
    "proxyupstream",
    "proxyupstreamserver",
    "proxysslcertificate",
    "proxyratelimit",
    "proxylocation",
    "proxydeployment",
)


class ProxyModelURLTestCase(TestCase):
    def test_navigation_add_button_routes_resolve(self):
        for model_url_name in MODEL_URL_NAMES:
            with self.subTest(model_url_name=model_url_name):
                url = reverse(f"plugins:netbox_proxy:{model_url_name}_add")
                self.assertTrue(url.endswith("/add/"))

    def test_standard_model_routes_resolve(self):
        for model_url_name in MODEL_URL_NAMES:
            with self.subTest(model_url_name=model_url_name):
                reverse(f"plugins:netbox_proxy:{model_url_name}_list")
                reverse(f"plugins:netbox_proxy:{model_url_name}", kwargs={"pk": 1})
                reverse(f"plugins:netbox_proxy:{model_url_name}_edit", kwargs={"pk": 1})
                reverse(
                    f"plugins:netbox_proxy:{model_url_name}_delete", kwargs={"pk": 1}
                )
                reverse(f"plugins:netbox_proxy:{model_url_name}_bulk_delete")
