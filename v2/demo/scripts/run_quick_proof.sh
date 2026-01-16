#!/bin/sh
set -eu
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT"

echo "==============================================================="
echo "VERA v2 — QUICK PROOF (LOCKED SURFACES)"
echo "==============================================================="
echo ""

echo "=== 0) TEST SUITE (must be green) ==="
pytest -q
echo ""

echo "=== 1) UNIVERSAL GOVERNANCE DEMO v1 ==="
v2/demo/scripts/demo_universal_governance_demo_v1.sh
echo ""

echo "=== 2) DOMAIN HATS v1 (fail-closed surface proof) ==="
v2/demo/scripts/demo_domain_hats_fail_closed_v1.sh
echo ""

echo "DONE"
