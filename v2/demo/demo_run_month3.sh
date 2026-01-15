#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

echo "=== VERA v2 Month 3 — One-Command Demo Run ==="
echo "ROOT: $ROOT"
echo

# Activate venv if present
if [[ -f "$ROOT/venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source "$ROOT/venv/bin/activate"
  echo "VENV: activated ($ROOT/venv)"
else
  echo "WARN: venv not found at $ROOT/venv (continuing without venv)"
fi
echo

echo "=== 1) UNIT TESTS ==="
python v2/tests/run_tests.py
echo

echo "=== 2) MONTH 3 DEMO VERIFICATION ==="
python v2/demo/demo_verify_month3.py
echo

echo "=== 3) QUICK WEB SANITY (optional) ==="
python - <<'PY'
from assistant.runtime.app import search_duckduckgo
q = "porsche 911"
res = search_duckduckgo(q, limit=3)
print("QUERY:", q)
print("LEN:", len(res))
for i, r in enumerate(res[:3], 1):
    print(f"{i}. {getattr(r,'title',None)} -> {getattr(r,'url',None)}")
PY
echo

echo "=== 4) LATEST DEBUG LOGS ==="
ls -1t v2/_pds/_debug | head -n 5 || true
echo

echo "PASS: Month 3 demo run complete."
echo "Next: run 'python run_vera_v2.py' for live voice demo."
