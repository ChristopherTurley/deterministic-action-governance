#!/bin/sh
set -eu
cd "$(dirname "$0")"
PYTHONPATH=. python3 v2/demo/trading_governance_demo.py
