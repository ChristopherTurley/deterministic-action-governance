#!/bin/sh
set -eu
cd "$(dirname "$0")/../.."
PYTHONPATH=. python3 v2/demo/focus_governance_demo.py
