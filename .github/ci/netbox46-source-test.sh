#!/usr/bin/env bash
# Run netbox_proxy tests against a cloned NetBox source tree.
#
# Required env vars:
#   NETBOX_REF          NetBox git tag/branch to clone (default: v4.6.0)
#   NETBOX_PLUGINS_JSON JSON array of plugin app names (e.g. '["netbox_nms","netbox_rpc","netbox_proxy"]')
#   MIGRATION_APPS      Space-separated app labels to check for pending migrations
#
# Optional env vars:
#   TEST_LABELS         Space-separated test labels (default: netbox_proxy)
#   NMS_REPO_DIR        Path to cloned netbox-nms checkout (default: /tmp/netbox-nms)
#   RPC_REPO_DIR        Path to cloned netbox-rpc checkout (default: /tmp/netbox-rpc)
#   NETBOX_SOURCE_DIR   Existing NetBox source tree (skips git clone when set)
#   DB_HOST / DB_NAME / DB_USER / DB_PASSWORD / DB_PORT
#   REDIS_HOST / REDIS_PORT / REDIS_PASSWORD / REDIS_CACHE_DATABASE

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
NETBOX_REF="${NETBOX_REF:-v4.6.0}"
WORK_BASE="${RUNNER_TEMP:-/tmp}/netbox-source-${NETBOX_REF#v}"
NETBOX_DIR="${NETBOX_SOURCE_DIR:-$WORK_BASE/netbox}"
VENV_DIR="${NETBOX_VENV_DIR:-$WORK_BASE/venv}"
CONFIG_DIR="$WORK_BASE/config"
PYTHON_BIN="${PYTHON_BIN:-python}"
NMS_REPO_DIR="${NMS_REPO_DIR:-/tmp/netbox-nms}"
RPC_REPO_DIR="${RPC_REPO_DIR:-/tmp/netbox-rpc}"

: "${NETBOX_PLUGINS_JSON:?Set NETBOX_PLUGINS_JSON, e.g. '[\"netbox_nms\",\"netbox_rpc\",\"netbox_proxy\"]'}"
: "${MIGRATION_APPS:?Set MIGRATION_APPS, e.g. 'netbox_nms netbox_rpc netbox_proxy'}"

# ── 1. Clone NetBox source ────────────────────────────────────────────────────

if [ -z "${NETBOX_SOURCE_DIR:-}" ]; then
  if [ ! -d "$NETBOX_DIR/.git" ]; then
    rm -rf "$NETBOX_DIR"
    git clone --depth=1 --branch "$NETBOX_REF" \
      https://github.com/netbox-community/netbox.git "$NETBOX_DIR"
  fi
else
  echo "Using NetBox source from NETBOX_SOURCE_DIR=$NETBOX_SOURCE_DIR"
fi

# ── 2. Create virtualenv ──────────────────────────────────────────────────────

rm -rf "$VENV_DIR"
"$PYTHON_BIN" -m venv "$VENV_DIR"
PY="$VENV_DIR/bin/python"

"$PY" -m pip install --upgrade pip wheel setuptools hatchling

# ── 3. Install NetBox requirements ────────────────────────────────────────────

"$PY" -m pip install -r "$NETBOX_DIR/requirements.txt"

# ── 4. Install plugin dependencies ──────────────────────────────────────────
# Install netbox-nms if the cloned checkout exists and is not the plugin root.

if [ -d "$NMS_REPO_DIR/netbox_nms" ] && [ "$NMS_REPO_DIR" != "$ROOT_DIR" ]; then
  echo "Installing netbox-nms from $NMS_REPO_DIR"
  "$PY" -m pip install --no-build-isolation -e "$NMS_REPO_DIR"
fi

if [ -d "$RPC_REPO_DIR/netbox_rpc" ] && [ "$RPC_REPO_DIR" != "$ROOT_DIR" ]; then
  echo "Installing netbox-rpc from $RPC_REPO_DIR"
  "$PY" -m pip install --no-build-isolation -e "$RPC_REPO_DIR"
fi

# ── 5. Install this plugin ────────────────────────────────────────────────────

"$PY" -m pip install --no-build-isolation -e "$ROOT_DIR"

# ── 6. Write NetBox configuration ─────────────────────────────────────────────

mkdir -p "$CONFIG_DIR"
cat > "$CONFIG_DIR/configuration.py" <<'PY'
import json
import os

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split()

DATABASES = {
    "default": {
        "NAME": os.environ.get("DB_NAME", "netbox"),
        "USER": os.environ.get("DB_USER", "netbox"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "netbox"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
        "CONN_MAX_AGE": 300,
    }
}

REDIS = {
    "tasks": {
        "HOST": os.environ.get("REDIS_HOST", "localhost"),
        "PORT": int(os.environ.get("REDIS_PORT", "6379")),
        "USERNAME": "",
        "PASSWORD": os.environ.get("REDIS_PASSWORD", ""),
        "DATABASE": int(os.environ.get("REDIS_DATABASE", "0")),
        "SSL": False,
    },
    "caching": {
        "HOST": os.environ.get("REDIS_HOST", "localhost"),
        "PORT": int(os.environ.get("REDIS_PORT", "6379")),
        "USERNAME": "",
        "PASSWORD": os.environ.get("REDIS_PASSWORD", ""),
        "DATABASE": int(os.environ.get("REDIS_CACHE_DATABASE", "1")),
        "SSL": False,
    },
}

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "netbox-source-ci-secret-key-not-for-production-000000000000",
)
API_TOKEN_PEPPERS = {
    1: "netbox-source-ci-pepper-not-for-production-000000000000000000",
}
DEFAULT_PERMISSIONS = {}
RQ = {"COMMIT_MODE": "auto"}

PLUGINS = json.loads(os.environ["NETBOX_PLUGINS_JSON"])
PLUGINS_CONFIG = {
    "netbox_nms": {
        "nms_backend_url": os.environ.get("NMS_BACKEND_URL", "http://nms-backend:8001"),
        "nms_backend_token": os.environ.get("NMS_BACKEND_TOKEN", "ci-token"),
    }
}
PY

export NETBOX_CONFIGURATION=configuration
export PYTHONPATH="$CONFIG_DIR:$NETBOX_DIR/netbox:$ROOT_DIR:$NMS_REPO_DIR:$RPC_REPO_DIR:${PYTHONPATH:-}"

# ── 7. Validate ───────────────────────────────────────────────────────────────

"$PY" "$NETBOX_DIR/netbox/manage.py" check
"$PY" "$NETBOX_DIR/netbox/manage.py" makemigrations $MIGRATION_APPS --check

# ── 8. Run tests ──────────────────────────────────────────────────────────────

TEST_LABELS="${TEST_LABELS:-netbox_proxy}"
"$PY" "$NETBOX_DIR/netbox/manage.py" test $TEST_LABELS -v 2
