from netbox.plugins.navigation import PluginMenu, PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

menu = PluginMenu(
    label="Proxy",
    groups=(
        (
            "Infrastructure",
            (
                PluginMenuItem(
                    link="plugins:netbox_proxy:proxycluster_list",
                    link_text="Clusters",
                    buttons=(
                        PluginMenuButton(
                            link="plugins:netbox_proxy:proxycluster_add",
                            title="Add",
                            icon_class="mdi mdi-plus-thick",
                            color=ButtonColorChoices.GREEN,
                        ),
                    ),
                ),
                PluginMenuItem(
                    link="plugins:netbox_proxy:proxynode_list",
                    link_text="Nodes",
                    buttons=(
                        PluginMenuButton(
                            link="plugins:netbox_proxy:proxynode_add",
                            title="Add",
                            icon_class="mdi mdi-plus-thick",
                            color=ButtonColorChoices.GREEN,
                        ),
                    ),
                ),
            ),
        ),
        (
            "Virtual Hosts",
            (
                PluginMenuItem(
                    link="plugins:netbox_proxy:proxyvhost_list",
                    link_text="VHosts",
                    buttons=(
                        PluginMenuButton(
                            link="plugins:netbox_proxy:proxyvhost_add",
                            title="Add",
                            icon_class="mdi mdi-plus-thick",
                            color=ButtonColorChoices.GREEN,
                        ),
                    ),
                ),
                PluginMenuItem(
                    link="plugins:netbox_proxy:proxylocation_list",
                    link_text="Locations",
                    buttons=(
                        PluginMenuButton(
                            link="plugins:netbox_proxy:proxylocation_add",
                            title="Add",
                            icon_class="mdi mdi-plus-thick",
                            color=ButtonColorChoices.GREEN,
                        ),
                    ),
                ),
            ),
        ),
        (
            "Upstreams",
            (
                PluginMenuItem(
                    link="plugins:netbox_proxy:proxyupstream_list",
                    link_text="Upstreams",
                    buttons=(
                        PluginMenuButton(
                            link="plugins:netbox_proxy:proxyupstream_add",
                            title="Add",
                            icon_class="mdi mdi-plus-thick",
                            color=ButtonColorChoices.GREEN,
                        ),
                    ),
                ),
                PluginMenuItem(
                    link="plugins:netbox_proxy:proxyupstreamserver_list",
                    link_text="Upstream Servers",
                    buttons=(
                        PluginMenuButton(
                            link="plugins:netbox_proxy:proxyupstreamserver_add",
                            title="Add",
                            icon_class="mdi mdi-plus-thick",
                            color=ButtonColorChoices.GREEN,
                        ),
                    ),
                ),
            ),
        ),
        (
            "SSL & Rate Limiting",
            (
                PluginMenuItem(
                    link="plugins:netbox_proxy:proxysslcertificate_list",
                    link_text="SSL Certificates",
                    buttons=(
                        PluginMenuButton(
                            link="plugins:netbox_proxy:proxysslcertificate_add",
                            title="Add",
                            icon_class="mdi mdi-plus-thick",
                            color=ButtonColorChoices.GREEN,
                        ),
                    ),
                ),
                PluginMenuItem(
                    link="plugins:netbox_proxy:proxyratelimit_list",
                    link_text="Rate Limits",
                    buttons=(
                        PluginMenuButton(
                            link="plugins:netbox_proxy:proxyratelimit_add",
                            title="Add",
                            icon_class="mdi mdi-plus-thick",
                            color=ButtonColorChoices.GREEN,
                        ),
                    ),
                ),
            ),
        ),
        (
            "Deployments",
            (
                PluginMenuItem(
                    link="plugins:netbox_proxy:proxydeployment_list",
                    link_text="Deployments",
                    buttons=(
                        PluginMenuButton(
                            link="plugins:netbox_proxy:proxydeployment_add",
                            title="Add",
                            icon_class="mdi mdi-plus-thick",
                            color=ButtonColorChoices.GREEN,
                        ),
                    ),
                ),
            ),
        ),
    ),
    icon_class="mdi mdi-swap-horizontal",
)
