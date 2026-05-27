from netbox.plugins import PluginConfig


class NetBoxProxyConfig(PluginConfig):
    name = "netbox_proxy"
    verbose_name = "NetBox Proxy"
    description = "NGINX reverse proxy configuration management for NMS"
    version = "0.1.0"
    base_url = "proxy"
    author = "Emerson Felipe"
    author_email = "emerson.felipe@nmultifibra.com.br"
    min_version = "4.5.0"
    max_version = "4.6.99"
    required_plugins = ["netbox_nms", "netbox_rpc"]
    required_settings = []
    default_settings = {}


config = NetBoxProxyConfig
