#!/bin/sh
set -eu
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT"

echo "==============================================================="
echo "VERA v2 — INVESTOR 5-MIN (LOCKED SURFACES)"
echo "==============================================================="
echo ""

echo "=== 0) TEST SUITE (must be green) ==="
pytest -q
echo ""

echo "=== 1) UNIVERSAL GOVERNANCE DEMO v1 ==="
v2/demo/scripts/demo_universal_governance_demo_v1.sh
echo ""

echo "=== 2) TRADING HAT v1 (typed harness) ==="
./demo_trading_hat_v1.sh
echo ""

echo "=== 3) FOCUS HAT v1 (typed harness) ==="
v2/demo/scripts/demo_focus_hat_v1.sh
echo ""

echo "=== 4) COAT v1 (stable reason->message templates) ==="
v2/demo/scripts/demo_coat_v1.sh
echo ""

echo "DONE"
