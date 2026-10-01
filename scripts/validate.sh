#!/usr/bin/env bash
set -euo pipefail
docker compose config >/dev/null
python -m compileall adapter/app adapter/tests
python -m json.tool grafana/dashboards/teamcenter-monitoring.json >/dev/null
echo "Validation passed"
