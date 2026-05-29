from netbox.plugins import PluginTemplateExtension


class DeviceProxyNodeTab(PluginTemplateExtension):
    models = ["dcim.device"]

    def right_page(self):
        device = self.context.get("object")
        if device is None:
            return ""
        from netbox_proxy.models import ProxyNode
        from django.contrib.contenttypes.models import ContentType

        ct = ContentType.objects.get_for_model(device)
        nodes = ProxyNode.objects.filter(
            assigned_object_type=ct,
            assigned_object_id=device.pk,
        ).select_related("cluster")
        return self.render(
            "netbox_proxy/inc/device_proxy_nodes.html",
            extra_context={"proxy_nodes": nodes},
        )


template_extensions = [DeviceProxyNodeTab]
