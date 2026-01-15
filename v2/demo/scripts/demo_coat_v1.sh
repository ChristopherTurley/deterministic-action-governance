#!/bin/sh
set -eu
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT"
PYTHONPATH=. python3 v2/demo/coat_v1_demo.py
