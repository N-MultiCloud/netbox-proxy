from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from netbox.models import NetBoxModel

from .choices import (
    DeployStatusChoices,
    LocationMatchTypeChoices,
    ProxyBalanceChoices,
    ProxyCertProviderChoices,
    ProxyProtocolChoices,
    ProxySSLModeChoices,
)


class ProxyCluster(NetBoxModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=500, blank=True)
    comments = models.TextField(blank=True)

    class Meta:
        app_label = "netbox_proxy"
        ordering = ("name",)
        verbose_name = "Proxy Cluster"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("plugins:netbox_proxy:proxycluster", args=[self.pk])


class ProxyNode(NetBoxModel):
    cluster = models.ForeignKey(
        ProxyCluster,
        on_delete=models.CASCADE,
        related_name="nodes",
    )
    name = models.CharField(max_length=255)
    assigned_object_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name="Assigned object type",
        null=True,
        blank=True,
    )
    assigned_object_id = models.PositiveBigIntegerField(
        verbose_name="Assigned object ID",
        null=True,
        blank=True,
    )
    assigned_object = GenericForeignKey(
        ct_field="assigned_object_type",
        fk_field="assigned_object_id",
    )
    management_ip = models.CharField(
        max_length=255,
        blank=True,
        help_text="Management IP or hostname used to reach this node",
    )
    nginx_config_path = models.CharField(
        max_length=500,
        blank=True,
        default="/etc/nginx",
        help_text="Filesystem path to the NGINX configuration directory",
    )
    nginx_binary = models.CharField(
        max_length=500,
        blank=True,
        default="/usr/sbin/nginx",
        help_text="Full path to the nginx binary on this node",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this node is currently active and receiving traffic",
    )
    last_seen = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp of the last successful health check or sync",
    )
    description = models.CharField(max_length=500, blank=True)
    comments = models.TextField(blank=True)

    class Meta:
        app_label = "netbox_proxy"
        ordering = ("cluster", "name")
        unique_together = (("cluster", "name"),)
        verbose_name = "Proxy Node"

    def __str__(self):
        return f"{self.cluster} / {self.name}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("plugins:netbox_proxy:proxynode", args=[self.pk])


class ProxyVHost(NetBoxModel):
    cluster = models.ForeignKey(
        ProxyCluster,
        on_delete=models.CASCADE,
        related_name="vhosts",
    )
    name = models.CharField(max_length=255)
    server_names = models.TextField(
        help_text="Space-separated NGINX server_name values (e.g. example.com *.example.com)",
    )
    listen_port = models.PositiveIntegerField(default=80)
    listen_ssl_port = models.PositiveIntegerField(
        default=443,
        help_text="Port used for HTTPS listeners",
    )
    ssl_mode = models.CharField(
        max_length=20,
        choices=ProxySSLModeChoices,
        default=ProxySSLModeChoices.OFF,
    )
    ssl_certificate = models.ForeignKey(
        "ProxySSLCertificate",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vhosts",
    )
    is_enabled = models.BooleanField(
        default=True,
        help_text="Whether this virtual host is active",
    )
    is_default_server = models.BooleanField(
        default=False,
        help_text="Add the default_server flag to the listen directive",
    )
    access_log = models.CharField(
        max_length=500,
        blank=True,
        help_text="Path to the access log file (leave blank to inherit)",
    )
    error_log = models.CharField(
        max_length=500,
        blank=True,
        help_text="Path to the error log file (leave blank to inherit)",
    )
    custom_directives = models.TextField(
        blank=True,
        help_text="Extra NGINX directives inserted verbatim into the server block",
    )
    description = models.CharField(max_length=500, blank=True)
    comments = models.TextField(blank=True)

    class Meta:
        app_label = "netbox_proxy"
        ordering = ("cluster", "name")
        unique_together = (("cluster", "name"),)
        verbose_name = "Proxy VHost"

    def __str__(self):
        return f"{self.cluster} / {self.name}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("plugins:netbox_proxy:proxyvhost", args=[self.pk])


class ProxyUpstream(NetBoxModel):
    cluster = models.ForeignKey(
        ProxyCluster,
        on_delete=models.CASCADE,
        related_name="upstreams",
    )
    name = models.CharField(max_length=255)
    protocol = models.CharField(
        max_length=20,
        choices=ProxyProtocolChoices,
        default=ProxyProtocolChoices.HTTP,
    )
    balance = models.CharField(
        max_length=20,
        choices=ProxyBalanceChoices,
        default=ProxyBalanceChoices.ROUND_ROBIN,
    )
    keepalive = models.PositiveIntegerField(
        default=0,
        help_text="Number of idle keepalive connections to upstream servers (0 = disabled)",
    )
    health_check_enabled = models.BooleanField(
        default=False,
        help_text="Enable active NGINX Plus / ngx_http_healthcheck_module health checks",
    )
    health_check_path = models.CharField(
        max_length=500,
        blank=True,
        default="/health",
        help_text="HTTP path used for active health checks",
    )
    health_check_interval = models.PositiveIntegerField(
        default=5,
        help_text="Interval in seconds between active health check requests",
    )
    custom_directives = models.TextField(
        blank=True,
        help_text="Extra NGINX directives inserted verbatim into the upstream block",
    )
    description = models.CharField(max_length=500, blank=True)
    comments = models.TextField(blank=True)

    class Meta:
        app_label = "netbox_proxy"
        ordering = ("cluster", "name")
        unique_together = (("cluster", "name"),)
        verbose_name = "Proxy Upstream"

    def __str__(self):
        return f"{self.cluster} / {self.name}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("plugins:netbox_proxy:proxyupstream", args=[self.pk])


class ProxyUpstreamServer(NetBoxModel):
    upstream = models.ForeignKey(
        ProxyUpstream,
        on_delete=models.CASCADE,
        related_name="servers",
    )
    address = models.CharField(
        max_length=255,
        help_text="Host:port or IP:port of the backend server",
    )
    weight = models.PositiveIntegerField(default=1)
    max_fails = models.PositiveIntegerField(default=3)
    fail_timeout = models.PositiveIntegerField(
        default=30,
        help_text="Fail timeout in seconds",
    )
    enabled = models.BooleanField(default=True)
    is_backup = models.BooleanField(
        default=False,
        help_text="Mark this server as a backup (only used when primary servers are unavailable)",
    )
    is_down = models.BooleanField(
        default=False,
        help_text="Permanently mark this server as unavailable (used for maintenance)",
    )
    description = models.CharField(max_length=500, blank=True)
    comments = models.TextField(blank=True)

    class Meta:
        app_label = "netbox_proxy"
        ordering = ("upstream", "address")
        unique_together = (("upstream", "address"),)
        verbose_name = "Proxy Upstream Server"

    def __str__(self):
        return f"{self.upstream} → {self.address}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("plugins:netbox_proxy:proxyupstreamserver", args=[self.pk])


class ProxySSLCertificate(NetBoxModel):
    name = models.CharField(max_length=255, unique=True)
    provider = models.CharField(
        max_length=20,
        choices=ProxyCertProviderChoices,
        default=ProxyCertProviderChoices.MANUAL,
    )
    domain = models.CharField(max_length=255)
    cert_path = models.CharField(
        max_length=500,
        blank=True,
        help_text="Filesystem path to the certificate file on proxy nodes",
    )
    key_path = models.CharField(
        max_length=500,
        blank=True,
        help_text="Filesystem path to the private key file on proxy nodes",
    )
    chain_path = models.CharField(
        max_length=500,
        blank=True,
        help_text="Filesystem path to the certificate chain/intermediate file",
    )
    auto_renew = models.BooleanField(
        default=False,
        help_text="Whether automatic renewal is configured for this certificate",
    )
    expires_at = models.DateTimeField(null=True, blank=True)
    custom_directives = models.TextField(
        blank=True,
        help_text="Extra NGINX SSL directives inserted verbatim into the server block",
    )
    description = models.CharField(max_length=500, blank=True)
    comments = models.TextField(blank=True)

    class Meta:
        app_label = "netbox_proxy"
        ordering = ("name",)
        verbose_name = "Proxy SSL Certificate"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("plugins:netbox_proxy:proxysslcertificate", args=[self.pk])


class ProxyRateLimit(NetBoxModel):
    name = models.CharField(max_length=255, unique=True)
    vhost = models.ForeignKey(
        "ProxyVHost",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rate_limits",
        help_text="VHost this rate limit zone is scoped to (leave blank for global)",
    )
    zone_name = models.CharField(
        max_length=255,
        blank=True,
        help_text="NGINX shared memory zone name for limit_req_zone (defaults to the object name if blank)",
    )
    key = models.CharField(
        max_length=255,
        blank=True,
        default="$binary_remote_addr",
        help_text="NGINX limit_req_zone key expression",
    )
    rate = models.CharField(
        max_length=50,
        help_text="NGINX limit_req_zone rate (e.g. 10r/s or 100r/m)",
    )
    burst = models.PositiveIntegerField(default=5)
    nodelay = models.BooleanField(
        default=False,
        help_text="Append nodelay to the limit_req directive",
    )
    description = models.CharField(max_length=500, blank=True)
    comments = models.TextField(blank=True)

    class Meta:
        app_label = "netbox_proxy"
        ordering = ("name",)
        verbose_name = "Proxy Rate Limit"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("plugins:netbox_proxy:proxyratelimit", args=[self.pk])


class ProxyLocation(NetBoxModel):
    vhost = models.ForeignKey(
        ProxyVHost,
        on_delete=models.CASCADE,
        related_name="locations",
    )
    path = models.CharField(max_length=500, help_text="URL path pattern")
    match_type = models.CharField(
        max_length=20,
        choices=LocationMatchTypeChoices,
        default=LocationMatchTypeChoices.MATCH_PREFIX,
    )
    upstream = models.ForeignKey(
        ProxyUpstream,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="locations",
    )
    rate_limit = models.ForeignKey(
        ProxyRateLimit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="locations",
    )
    proxy_pass_url = models.CharField(
        max_length=500,
        blank=True,
        help_text="Explicit proxy_pass URL (overrides upstream if set)",
    )
    proxy_set_headers = models.JSONField(
        default=dict,
        blank=True,
        help_text='Header overrides, e.g. {"Host": "$host", "X-Real-IP": "$remote_addr"}',
    )
    sort_order = models.PositiveIntegerField(
        default=100,
        help_text="Render order within the server block (lower values rendered first)",
    )
    custom_directives = models.TextField(
        blank=True,
        help_text="Extra NGINX directives inserted verbatim into the location block",
    )
    description = models.CharField(max_length=500, blank=True)
    comments = models.TextField(blank=True)

    class Meta:
        app_label = "netbox_proxy"
        ordering = ("vhost", "path")
        unique_together = (("vhost", "path"),)
        verbose_name = "Proxy Location"

    def __str__(self):
        return f"{self.vhost} {self.path}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("plugins:netbox_proxy:proxylocation", args=[self.pk])


class ProxyDeployment(NetBoxModel):
    cluster = models.ForeignKey(
        ProxyCluster,
        on_delete=models.CASCADE,
        related_name="deployments",
    )
    node = models.ForeignKey(
        ProxyNode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="deployments",
        help_text="Specific node targeted by this deployment (null = cluster-wide)",
    )
    status = models.CharField(
        max_length=20,
        choices=DeployStatusChoices,
        default=DeployStatusChoices.STATUS_PENDING,
    )
    initiated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    rpc_execution = models.ForeignKey(
        "netbox_rpc.RPCExecution",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="proxy_deployments",
    )
    config_snapshot = models.TextField(
        blank=True,
        help_text="The rendered NGINX configuration at deployment time",
    )
    previous_config = models.TextField(
        blank=True,
        help_text="The NGINX configuration that was active before this deployment",
    )
    started_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the deployment execution started",
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the deployment execution finished",
    )
    error_message = models.TextField(blank=True)
    description = models.CharField(max_length=500, blank=True)
    comments = models.TextField(blank=True)

    class Meta:
        app_label = "netbox_proxy"
        ordering = ("-created",)
        verbose_name = "Proxy Deployment"

    def __str__(self):
        return f"{self.cluster} deployment #{self.pk}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("plugins:netbox_proxy:proxydeployment", args=[self.pk])
