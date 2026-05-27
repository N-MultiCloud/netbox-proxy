from netbox.api.serializers import NetBoxModelSerializer
from rest_framework import serializers

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


class ProxyClusterSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_proxy-api:proxycluster-detail"
    )

    class Meta:
        model = ProxyCluster
        fields = ("id", "url", "display", "name", "description", "tags", "custom_fields", "created", "last_updated")


class ProxyNodeSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_proxy-api:proxynode-detail"
    )
    cluster = ProxyClusterSerializer(nested=True)

    class Meta:
        model = ProxyNode
        fields = (
            "id", "url", "display",
            "cluster",
            "name",
            "assigned_object_type",
            "assigned_object_id",
            "management_ip",
            "nginx_config_path",
            "nginx_binary",
            "is_active",
            "last_seen",
            "description",
            "tags", "custom_fields", "created", "last_updated",
        )


class ProxySSLCertificateSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_proxy-api:proxysslcertificate-detail"
    )

    class Meta:
        model = ProxySSLCertificate
        fields = (
            "id", "url", "display",
            "name", "provider", "domain",
            "cert_path", "key_path", "chain_path",
            "auto_renew", "expires_at",
            "custom_directives",
            "description",
            "tags", "custom_fields", "created", "last_updated",
        )


class ProxyVHostSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_proxy-api:proxyvhost-detail"
    )
    cluster = ProxyClusterSerializer(nested=True)
    ssl_certificate = ProxySSLCertificateSerializer(nested=True, read_only=True)
    ssl_certificate_id = serializers.PrimaryKeyRelatedField(
        queryset=ProxySSLCertificate.objects.all(),
        source="ssl_certificate",
        allow_null=True,
        required=False,
    )

    class Meta:
        model = ProxyVHost
        fields = (
            "id", "url", "display",
            "cluster",
            "name", "server_names", "listen_port", "listen_ssl_port",
            "ssl_mode", "ssl_certificate", "ssl_certificate_id",
            "is_enabled", "is_default_server",
            "access_log", "error_log",
            "custom_directives",
            "description",
            "tags", "custom_fields", "created", "last_updated",
        )


class ProxyUpstreamSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_proxy-api:proxyupstream-detail"
    )
    cluster = ProxyClusterSerializer(nested=True)

    class Meta:
        model = ProxyUpstream
        fields = (
            "id", "url", "display",
            "cluster", "name", "protocol", "balance",
            "keepalive", "health_check_enabled", "health_check_path", "health_check_interval",
            "custom_directives",
            "description",
            "tags", "custom_fields", "created", "last_updated",
        )


class ProxyUpstreamServerSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_proxy-api:proxyupstreamserver-detail"
    )
    upstream = ProxyUpstreamSerializer(nested=True)

    class Meta:
        model = ProxyUpstreamServer
        fields = (
            "id", "url", "display",
            "upstream", "address", "weight", "max_fails", "fail_timeout",
            "enabled", "is_backup", "is_down",
            "description",
            "tags", "custom_fields", "created", "last_updated",
        )


class ProxyRateLimitSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_proxy-api:proxyratelimit-detail"
    )
    vhost = ProxyVHostSerializer(nested=True, read_only=True)
    vhost_id = serializers.PrimaryKeyRelatedField(
        queryset=ProxyVHost.objects.all(),
        source="vhost",
        allow_null=True,
        required=False,
    )

    class Meta:
        model = ProxyRateLimit
        fields = (
            "id", "url", "display",
            "name", "vhost", "vhost_id", "zone_name", "key",
            "rate", "burst", "nodelay",
            "description",
            "tags", "custom_fields", "created", "last_updated",
        )


class ProxyLocationSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_proxy-api:proxylocation-detail"
    )
    vhost = ProxyVHostSerializer(nested=True)
    upstream = ProxyUpstreamSerializer(nested=True, read_only=True)
    upstream_id = serializers.PrimaryKeyRelatedField(
        queryset=ProxyUpstream.objects.all(),
        source="upstream",
        allow_null=True,
        required=False,
    )
    rate_limit = ProxyRateLimitSerializer(nested=True, read_only=True)

    class Meta:
        model = ProxyLocation
        fields = (
            "id", "url", "display",
            "vhost", "path", "match_type",
            "upstream", "upstream_id", "rate_limit",
            "proxy_pass_url", "proxy_set_headers", "sort_order",
            "custom_directives",
            "description",
            "tags", "custom_fields", "created", "last_updated",
        )


class ProxyDeploymentSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_proxy-api:proxydeployment-detail"
    )
    cluster = ProxyClusterSerializer(nested=True)
    node = ProxyNodeSerializer(nested=True, read_only=True)

    class Meta:
        model = ProxyDeployment
        fields = (
            "id", "url", "display",
            "cluster", "node", "status", "initiated_by", "rpc_execution",
            "config_snapshot", "previous_config",
            "started_at", "completed_at",
            "error_message",
            "description",
            "tags", "custom_fields", "created", "last_updated",
        )
