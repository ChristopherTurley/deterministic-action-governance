#!/usr/bin/env bash
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

PYTHONPATH=. python3 v2/demo/universal_governance_demo_v1.py
