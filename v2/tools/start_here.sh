#!/usr/bin/env bash
set -euo pipefail

export PYTHONPATH="."
cd "$(dirname "$0")/../.." || exit 1

echo "============================================================"
echo "VERA v2 — COMMERCIAL BUNDLE v1 (START HERE)"
echo "============================================================"
echo

if command -v git >/dev/null 2>&1; then
  echo "COMMIT: $(git rev-parse --short HEAD 2>/dev/null || echo unknown)"
  echo
fi

echo "1) RUN COMMERCIAL SUITE (must be green)"
bash v2/tools/run_commercial_suite_v1.sh
echo

echo "2) DEVICE-B VERIFY (must be OK)"
python v2/device_b/verify_all.py
echo

echo "3) BUNDLE SNAPSHOT + MANIFEST"
python - <<'PYY'
import json
from pathlib import Path

snap = Path("v2/bundles/commercial_bundle_v1/BUNDLE_SNAPSHOT.json")
man  = Path("v2/device_b/MANIFEST.json")

print("BUNDLE_SNAPSHOT:", str(snap) if snap.exists() else "MISSING")
print("DEVICE_B_MANIFEST:", str(man) if man.exists() else "MISSING")

if snap.exists():
    d = json.loads(snap.read_text(encoding="utf-8"))
    hats = d.get("bundle_members") or d.get("members") or d.get("hats") or []
    if isinstance(hats, dict):
        hats = list(hats.keys())
    if not isinstance(hats, list):
        hats = []
    hats = [str(x) for x in hats]
    print("BUNDLE_MEMBERS:", ", ".join(hats) if hats else "(none parsed)")
PYY
echo

echo "4) EVALUATOR DOCS (open these)"
echo " - v2/docs/public/REPO_MAP_COMMERCIAL_V1.md"
echo " - v2/docs/public/COMMERCIAL_BUNDLE_V1.md"
echo " - v2/sales/COMPLIANCE_GRADE_SALES_BRIEF_V1.md"
echo " - v2/sales/PROCUREMENT_COVER_MEMO_V1.md"
echo " - v2/legal/VERA_COMMERCIAL_BUNDLE_V1_LICENSE.md"
echo " - v2/legal/PROCUREMENT_RIDER_ONE_PAGER.md"
echo

echo "DONE: If steps 1–2 are green/OK, the artifact is procurement-ready."
