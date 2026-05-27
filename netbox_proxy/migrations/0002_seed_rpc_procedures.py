from django.db import migrations

PROXY_RPC_PROCEDURES = (
    {
        "name": "service.nginx.1.config_test",
        "handler_id": "service.nginx.config_test",
        "target_models": ["dcim.device"],
        "effect": "read",
        "timeout_seconds": 30,
        "approval_required": False,
        "params_schema": {
            "type": "object",
            "required": ["node_id"],
            "additionalProperties": False,
            "properties": {
                "node_id": {"type": "integer", "minimum": 1},
            },
        },
        "result_schema": {
            "type": "object",
            "required": ["ok", "procedure", "target"],
            "properties": {
                "ok": {"type": "boolean"},
                "procedure": {"type": "string"},
                "target": {"type": "string"},
                "config_valid": {"type": "boolean"},
                "output": {"type": "string"},
            },
        },
        "description": "Run nginx -t to validate configuration on a proxy node",
    },
    {
        "name": "service.nginx.1.config_deploy",
        "handler_id": "service.nginx.config_deploy",
        "target_models": ["dcim.device"],
        "effect": "write",
        "timeout_seconds": 120,
        "approval_required": False,
        "params_schema": {
            "type": "object",
            "required": ["node_id", "config_content", "deployment_id"],
            "additionalProperties": False,
            "properties": {
                "node_id": {"type": "integer", "minimum": 1},
                "config_content": {"type": "string", "minLength": 1},
                "deployment_id": {"type": "integer", "minimum": 1},
                "config_path": {"type": "string"},
            },
        },
        "result_schema": {
            "type": "object",
            "required": ["ok", "procedure", "target"],
            "properties": {
                "ok": {"type": "boolean"},
                "procedure": {"type": "string"},
                "target": {"type": "string"},
                "config_valid": {"type": "boolean"},
                "deployed_path": {"type": "string"},
            },
        },
        "description": "Write rendered NGINX config to a proxy node, test, and activate",
    },
    {
        "name": "service.nginx.1.reload",
        "handler_id": "service.nginx.reload",
        "target_models": ["dcim.device"],
        "effect": "write",
        "timeout_seconds": 30,
        "approval_required": False,
        "params_schema": {
            "type": "object",
            "required": ["node_id"],
            "additionalProperties": False,
            "properties": {
                "node_id": {"type": "integer", "minimum": 1},
            },
        },
        "result_schema": {
            "type": "object",
            "required": ["ok", "procedure", "target"],
            "properties": {
                "ok": {"type": "boolean"},
                "procedure": {"type": "string"},
                "target": {"type": "string"},
            },
        },
        "description": "Execute systemctl reload nginx on a proxy node",
    },
    {
        "name": "service.nginx.1.rollback",
        "handler_id": "service.nginx.rollback",
        "target_models": ["dcim.device"],
        "effect": "write",
        "timeout_seconds": 120,
        "approval_required": False,
        "params_schema": {
            "type": "object",
            "required": ["node_id", "deployment_id", "previous_config"],
            "additionalProperties": False,
            "properties": {
                "node_id": {"type": "integer", "minimum": 1},
                "deployment_id": {"type": "integer", "minimum": 1},
                "previous_config": {"type": "string", "minLength": 1},
            },
        },
        "result_schema": {
            "type": "object",
            "required": ["ok", "procedure", "target"],
            "properties": {
                "ok": {"type": "boolean"},
                "procedure": {"type": "string"},
                "target": {"type": "string"},
                "rolled_back_deployment": {"type": "integer"},
            },
        },
        "description": "Restore previous NGINX config snapshot and reload",
    },
)


def seed_proxy_rpc_procedures(apps, schema_editor):
    RPCProcedure = apps.get_model("netbox_rpc", "RPCProcedure")
    for item in PROXY_RPC_PROCEDURES:
        defaults = dict(item)
        name = defaults.pop("name")
        RPCProcedure.objects.update_or_create(name=name, defaults=defaults)


def unseed_proxy_rpc_procedures(apps, schema_editor):
    RPCProcedure = apps.get_model("netbox_rpc", "RPCProcedure")
    RPCProcedure.objects.filter(
        name__in=[item["name"] for item in PROXY_RPC_PROCEDURES]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("netbox_proxy", "0001_initial"),
        ("netbox_rpc", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_proxy_rpc_procedures, unseed_proxy_rpc_procedures),
    ]
