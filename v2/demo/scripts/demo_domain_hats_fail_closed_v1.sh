#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$REPO_ROOT"

export PYTHONPATH="."

python3 v2/demo/domain_hats_fail_closed_demo_v1.py
