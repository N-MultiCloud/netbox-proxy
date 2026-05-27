# AGENTS.md — netbox-proxy

## Agent Quick Reference

- Package: `netbox-proxy` (import: `netbox_proxy`)
- Python >= 3.12, NetBox 4.5.0 – 4.6.99
- Required plugins: `netbox-nms`, `netbox-rpc`
- 9 models: ProxyCluster, ProxyNode, ProxyVHost, ProxyLocation, ProxyUpstream, ProxyUpstreamServer, ProxySSLCertificate, ProxyRateLimit, ProxyDeployment
- Tests: `python manage.py test netbox_proxy -v 2` (requires NetBox env)
- Lint: `ruff check . && ruff format --check .`
- No direct SSH — all execution delegated to netbox-rpc
- ProxyNode uses GFK pattern (assigned_object_type + assigned_object_id)
- DeployStatusChoices: pending, rendering, testing, deploying, reloading, success, failed, rolled_back
