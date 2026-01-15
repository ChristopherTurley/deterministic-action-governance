#!/bin/sh
set -eu
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT"
PYTHONPATH=. python3 v2/bridge/run_hat_session.py \
  --hat FOCUS_HAT_V1 \
  --context '{"focus_mode":"DEEP_WORK","task_count_cap":5,"tasks_remaining":3,"minutes_cap":60,"minutes_remaining":45,"context_ttl_seconds":600}' \
  --proposal '{"task_count":2,"planned_minutes":30}' \
  --commit '{"task_count":3,"planned_minutes":30}'
