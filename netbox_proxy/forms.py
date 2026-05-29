from django import forms
from django.contrib.contenttypes.models import ContentType
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, ContentTypeChoiceField, DynamicModelChoiceField

from .choices import (
    DeployStatusChoices,
    LocationMatchTypeChoices,
    ProxyBalanceChoices,
    ProxyCertProviderChoices,
    ProxyProtocolChoices,
    ProxySSLModeChoices,
)
from .models import (
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


class ProxyClusterForm(NetBoxModelForm):
    comments = CommentField()

    class Meta:
        model = ProxyCluster
        fields = ("name", "description", "tags", "comments")


class ProxyNodeForm(NetBoxModelForm):
    cluster = DynamicModelChoiceField(queryset=ProxyCluster.objects.all())
    assigned_object_type = ContentTypeChoiceField(
        queryset=ContentType.objects.filter(model__in=["device", "virtualmachine"]),
        required=False,
        label="Assigned object type",
    )
    comments = CommentField()

    class Meta:
        model = ProxyNode
        fields = (
            "cluster",
            "name",
            "assigned_object_type",
            "assigned_object_id",
            "management_ip",
            "nginx_config_path",
            "nginx_binary",
            "is_active",
            "description",
            "tags",
            "comments",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show a hint of the currently-linked object in the description
        if self.instance and self.instance.pk and self.instance.assigned_object:
            obj = self.instance.assigned_object
            self.fields["assigned_object_id"].help_text = (
                f"Currently linked to: {obj}"
            )


class ProxyVHostForm(NetBoxModelForm):
    cluster = DynamicModelChoiceField(queryset=ProxyCluster.objects.all())
    ssl_certificate = DynamicModelChoiceField(
        queryset=ProxySSLCertificate.objects.all(),
        required=False,
    )
    comments = CommentField()

    class Meta:
        model = ProxyVHost
        fields = (
            "cluster",
            "name",
            "server_names",
            "listen_port",
            "listen_ssl_port",
            "ssl_mode",
            "ssl_certificate",
            "is_enabled",
            "is_default_server",
            "access_log",
            "error_log",
            "custom_directives",
            "description",
            "tags",
            "comments",
        )


class ProxyUpstreamForm(NetBoxModelForm):
    cluster = DynamicModelChoiceField(queryset=ProxyCluster.objects.all())
    comments = CommentField()

    class Meta:
        model = ProxyUpstream
        fields = (
            "cluster",
            "name",
            "protocol",
            "balance",
            "keepalive",
            "health_check_enabled",
            "health_check_path",
            "health_check_interval",
            "custom_directives",
            "description",
            "tags",
            "comments",
        )


class ProxyUpstreamServerForm(NetBoxModelForm):
    upstream = DynamicModelChoiceField(queryset=ProxyUpstream.objects.all())
    comments = CommentField()

    class Meta:
        model = ProxyUpstreamServer
        fields = (
            "upstream",
            "address",
            "weight",
            "max_fails",
            "fail_timeout",
            "enabled",
            "is_backup",
            "is_down",
            "description",
            "tags",
            "comments",
        )


class ProxySSLCertificateForm(NetBoxModelForm):
    comments = CommentField()

    class Meta:
        model = ProxySSLCertificate
        fields = (
            "name",
            "provider",
            "domain",
            "cert_path",
            "key_path",
            "chain_path",
            "auto_renew",
            "expires_at",
            "custom_directives",
            "description",
            "tags",
            "comments",
        )
        widgets = {
            "expires_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class ProxyRateLimitForm(NetBoxModelForm):
    vhost = DynamicModelChoiceField(queryset=ProxyVHost.objects.all(), required=False)
    comments = CommentField()

    class Meta:
        model = ProxyRateLimit
        fields = (
            "name",
            "vhost",
            "zone_name",
            "key",
            "rate",
            "burst",
            "nodelay",
            "description",
            "tags",
            "comments",
        )


class ProxyLocationForm(NetBoxModelForm):
    vhost = DynamicModelChoiceField(queryset=ProxyVHost.objects.all())
    upstream = DynamicModelChoiceField(queryset=ProxyUpstream.objects.all(), required=False)
    rate_limit = DynamicModelChoiceField(queryset=ProxyRateLimit.objects.all(), required=False)
    comments = CommentField()

    class Meta:
        model = ProxyLocation
        fields = (
            "vhost",
            "path",
            "match_type",
            "upstream",
            "rate_limit",
            "proxy_pass_url",
            "proxy_set_headers",
            "sort_order",
            "custom_directives",
            "description",
            "tags",
            "comments",
        )


class ProxyDeploymentForm(NetBoxModelForm):
    cluster = DynamicModelChoiceField(queryset=ProxyCluster.objects.all())
    node = DynamicModelChoiceField(queryset=ProxyNode.objects.all(), required=False)
    comments = CommentField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Import lazily to avoid circular dependency at module load time
        from netbox_rpc.models import RPCExecution
        self.fields["rpc_execution"] = DynamicModelChoiceField(
            queryset=RPCExecution.objects.all(),
            required=False,
            label="RPC Execution",
        )

    class Meta:
        model = ProxyDeployment
        fields = ("cluster", "node", "rpc_execution", "description", "tags", "comments")


# ── Filter forms ────────────────────────────────────────────────────────────

class ProxyClusterFilterForm(NetBoxModelFilterSetForm):
    model = ProxyCluster
    tag = forms.MultipleChoiceField(required=False)


class ProxyNodeFilterForm(NetBoxModelFilterSetForm):
    model = ProxyNode
    cluster_id = DynamicModelChoiceField(
        queryset=ProxyCluster.objects.all(),
        required=False,
        label="Cluster",
    )
    is_active = forms.NullBooleanField(required=False)


class ProxyVHostFilterForm(NetBoxModelFilterSetForm):
    model = ProxyVHost
    cluster_id = DynamicModelChoiceField(
        queryset=ProxyCluster.objects.all(),
        required=False,
        label="Cluster",
    )
    ssl_mode = forms.ChoiceField(
        choices=[("", "---------")] + list(ProxySSLModeChoices),
        required=False,
    )
    is_enabled = forms.NullBooleanField(required=False)


class ProxyUpstreamFilterForm(NetBoxModelFilterSetForm):
    model = ProxyUpstream
    cluster_id = DynamicModelChoiceField(
        queryset=ProxyCluster.objects.all(),
        required=False,
        label="Cluster",
    )
    protocol = forms.ChoiceField(
        choices=[("", "---------")] + list(ProxyProtocolChoices),
        required=False,
    )
    balance = forms.ChoiceField(
        choices=[("", "---------")] + list(ProxyBalanceChoices),
        required=False,
    )


class ProxyUpstreamServerFilterForm(NetBoxModelFilterSetForm):
    model = ProxyUpstreamServer
    upstream_id = DynamicModelChoiceField(
        queryset=ProxyUpstream.objects.all(),
        required=False,
        label="Upstream",
    )
    enabled = forms.NullBooleanField(required=False)
    is_backup = forms.NullBooleanField(required=False)
    is_down = forms.NullBooleanField(required=False)


class ProxySSLCertificateFilterForm(NetBoxModelFilterSetForm):
    model = ProxySSLCertificate
    provider = forms.ChoiceField(
        choices=[("", "---------")] + list(ProxyCertProviderChoices),
        required=False,
    )


class ProxyRateLimitFilterForm(NetBoxModelFilterSetForm):
    model = ProxyRateLimit
    vhost_id = DynamicModelChoiceField(
        queryset=ProxyVHost.objects.all(),
        required=False,
        label="VHost",
    )


class ProxyLocationFilterForm(NetBoxModelFilterSetForm):
    model = ProxyLocation
    vhost_id = DynamicModelChoiceField(
        queryset=ProxyVHost.objects.all(),
        required=False,
        label="VHost",
    )
    match_type = forms.ChoiceField(
        choices=[("", "---------")] + list(LocationMatchTypeChoices),
        required=False,
    )


class ProxyDeploymentFilterForm(NetBoxModelFilterSetForm):
    model = ProxyDeployment
    cluster_id = DynamicModelChoiceField(
        queryset=ProxyCluster.objects.all(),
        required=False,
        label="Cluster",
    )
    node_id = DynamicModelChoiceField(
        queryset=ProxyNode.objects.all(),
        required=False,
        label="Node",
    )
    status = forms.ChoiceField(
        choices=[("", "---------")] + list(DeployStatusChoices),
        required=False,
    )
