#!/bin/sh
set -eu
cd "$(dirname "$0")/../.."
PYTHONPATH=. python3 v2/demo/coat_v1_demo.py
