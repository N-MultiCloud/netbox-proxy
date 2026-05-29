"""Set approval_required=True for nginx write procedures seeded by migration 0002.

The original seed left all four procedures with approval_required=False, which
allowed any user with execute_rpcprocedure to deploy, reload, or roll back
NGINX configurations on production hosts without a second approver.

Only the read-only config_test procedure remains unapproved. The three write
procedures (config_deploy, reload, rollback) now require approve_rpcprocedure.
"""

from django.db import migrations

NGINX_WRITE_PROCEDURES = (
    "service.nginx.1.config_deploy",
    "service.nginx.1.reload",
    "service.nginx.1.rollback",
)


def set_nginx_write_approval_required(apps, schema_editor):
    RPCProcedure = apps.get_model("netbox_rpc", "RPCProcedure")
    RPCProcedure.objects.filter(name__in=NGINX_WRITE_PROCEDURES).update(
        approval_required=True
    )


def unset_nginx_write_approval_required(apps, schema_editor):
    RPCProcedure = apps.get_model("netbox_rpc", "RPCProcedure")
    RPCProcedure.objects.filter(name__in=NGINX_WRITE_PROCEDURES).update(
        approval_required=False
    )


class Migration(migrations.Migration):
    dependencies = [
        ("netbox_proxy", "0002_seed_rpc_procedures"),
    ]

    operations = [
        migrations.RunPython(
            set_nginx_write_approval_required,
            unset_nginx_write_approval_required,
        ),
    ]
