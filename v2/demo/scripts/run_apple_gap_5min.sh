#!/bin/sh
set -eu
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT"

echo "==============================================================="
echo "VERA v2 — APPLE GAP 5-MIN (LOCKED SURFACES)"
echo "==============================================================="
echo ""

echo "=== 0) TEST SUITE (must be green) ==="
pytest -q
echo ""

echo "=== 1) UNIVERSAL GOVERNANCE DEMO v1 ==="
v2/demo/scripts/demo_universal_governance_demo_v1.sh
echo ""

echo "=== 2) MULTI-HAT ROUTER v1 (explicit selection only) ==="
v2/demo/scripts/demo_multi_hat_router_v1.sh
echo ""

echo "=== 3) DOMAIN HATS v1 (fail-closed surface proof) ==="
v2/demo/scripts/demo_domain_hats_fail_closed_v1.sh
echo ""

echo "=== 4) COAT v1 (stable reason->message templates) ==="
v2/demo/scripts/demo_coat_v1.sh
echo ""

echo "DONE"
