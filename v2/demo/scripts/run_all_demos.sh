#!/bin/sh
set -eu

ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT"

echo "==============================================================="
echo "VERA v2 — RUN ALL DEMOS (LOCKED SURFACES)"
echo "==============================================================="
echo ""

echo "=== 0) TEST SUITE (must be green) ==="
pytest -q
echo ""

echo "=== 1) WEEK 2 TRADING HAT HARNESS (3 scenarios) ==="
./demo_trading_hat_v1.sh
echo ""

echo "=== 2) WEEK 3 TRADING OPEN SESSION QUICK DEMO (ALLOW + DRIFT) ==="
./demo_trading_live_quick.sh
echo ""

echo "=== 3) SPOKEN TRADING DEMO RUNNER (opt-in voice, v1 untouched) ==="
PYTHONPATH=. python3 v2/demo/trading_live_spoken_demo.py
echo ""

echo "=== 4) FOCUS HAT DEMO (second hat) ==="
if [ -x v2/demo/scripts/demo_focus_hat_v1.sh ]; then
  v2/demo/scripts/demo_focus_hat_v1.sh
else
  echo "MISSING: v2/demo/scripts/demo_focus_hat_v1.sh"
fi
echo ""

echo "=== 5) MULTI-HAT ROUTER v1 DEMO (explicit selection only) ==="
v2/demo/scripts/demo_multi_hat_router_v1.sh
echo ""

echo "=== 6) COAT v1 DEMO (stable reason->message templates) ==="
v2/demo/scripts/demo_coat_v1.sh
echo ""

echo "=== 7) BRIDGE v1 DEMOS (opt-in CLI; v1 unchanged) ==="
echo "--- Trading (drift -> REQUIRE_RECOMMIT) ---"
v2/demo/scripts/demo_bridge_trading_hat.sh || true
echo ""
echo "--- Focus (drift -> REQUIRE_RECOMMIT) ---"
v2/demo/scripts/demo_bridge_focus_hat.sh || true
echo ""

echo "==============================================================="
echo "DONE"
echo "==============================================================="
