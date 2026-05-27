# CLAUDE.md — netbox-proxy

## Workspace Context

This file lives at the root of the `netbox-proxy` repository.
Workspace guidance: `/root/personal-context/CLAUDE.md`.
Per-repo deep-dive: `/root/personal-context/claude-reference/netbox-proxy.md` (once created).
Submodule layout and cross-repo links: `/root/personal-context/claude-reference/dependency-map.md`.

## Project Overview

NetBox plugin for managing NGINX reverse proxy configuration as structured data.
NetBox is the single source of truth for all proxy state; SSH execution is
entirely delegated to `netbox-rpc` + `nms-backend` RPC handlers.

Package: `netbox-proxy` (import: `netbox_proxy`)
Version: 0.1.0
Python: >= 3.12
NetBox: 4.5.0 – 4.6.99
Required plugins: `netbox-nms >= 0.1.2`, `netbox-rpc >= 0.1.0`

## Models (9)

| Model | Purpose |
|---|---|
| `ProxyCluster` | Logical grouping of NGINX hosts |
| `ProxyNode` | Individual NGINX host machine (GFK → Device or VirtualMachine) |
| `ProxyVHost` | server block / virtual host |
| `ProxyLocation` | location block within a vhost |
| `ProxyUpstream` | upstream block |
| `ProxyUpstreamServer` | backend server in an upstream |
| `ProxySSLCertificate` | TLS certificate configuration |
| `ProxyRateLimit` | rate limiting zone |
| `ProxyDeployment` | deployment audit record (FK → RPCExecution) |

## RPC Procedures (seeded by migration 0002)

| handler_id | name |
|---|---|
| `service.nginx.config_test` | `service.nginx.1.config_test` |
| `service.nginx.config_deploy` | `service.nginx.1.config_deploy` |
| `service.nginx.reload` | `service.nginx.1.reload` |
| `service.nginx.rollback` | `service.nginx.1.rollback` |

## REST API

Base path: `/api/plugins/proxy/`
Standard CRUD for all 9 models.

## Navigation Menu

**Infrastructure**: Clusters, Nodes
**Configuration**: Virtual Hosts, Upstreams, Upstream Servers, SSL Certificates, Rate Limits, Locations
**Operations**: Deployments

## Integration Points

- **nms-backend**: Plugin proxy at `/netbox/netbox-proxy/plugin/*`, orchestration at `/proxy/*` (render, deploy, rollback), Jinja2 renderer
- **nms**: Frontend pages at `/proxy/*` (clusters, nodes, vhosts, upstreams, ssl, deployments)
- **netbox-rpc**: Deployment creates RPCExecution records for SSH-backed nginx operations
- **netbox-nms**: Backend service connections and device credentials

## Commands

```bash
ruff check .
ruff format --check .
python -m compileall netbox_proxy
# Tests require NetBox environment:
python manage.py test netbox_proxy -v 2
```

## File Layout

```
netbox_proxy/
  __init__.py          # PluginConfig
  choices.py           # ChoiceSets
  models.py            # 9 NetBoxModel subclasses
  forms.py             # NetBoxModelForm per model
  tables.py            # NetBoxTable per model
  filtersets.py        # NetBoxModelFilterSet per model
  views.py             # CRUD views
  urls.py              # urlpatterns
  navigation.py        # PluginMenu
  search.py            # SearchIndex per model
  template_content.py  # Device detail extension
  api/
    urls.py
    serializers.py
    views.py
  graphql/
    types.py
    schema.py
    filters.py
  templates/netbox_proxy/  # 9 detail templates
  migrations/
    0001_initial.py
    0002_seed_rpc_procedures.py
  tests/
    test_models.py
    test_api.py
    test_filtersets.py
    test_forms.py
    test_views.py
```
