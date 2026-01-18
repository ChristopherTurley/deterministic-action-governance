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

def _normalize_members(obj):
    if obj is None:
        return []
    if isinstance(obj, dict):
        return list(obj.keys())
    if isinstance(obj, list):
        out = []
        for x in obj:
            if isinstance(x, str):
                out.append(x)
            elif isinstance(x, dict):
                for k in ("id","name","hat","hat_id","hat_name","key","code"):
                    v = x.get(k)
                    if isinstance(v, str) and v.strip():
                        out.append(v.strip())
                        break
        return out
    return []

members = []
if snap.exists():
    d = json.loads(snap.read_text(encoding="utf-8"))
    candidates = []
    if isinstance(d, dict):
        # Try common keys + any key containing "member"
        for k in ("bundle_members","members","hats","bundle","commercial_bundle","bundle_v1","bundle_items"):
            if k in d:
                candidates.append(d.get(k))
        for k in d.keys():
            if isinstance(k, str) and "member" in k.lower():
                candidates.append(d.get(k))
    for c in candidates:
        members = _normalize_members(c)
        if members:
            break

if members:
    members = sorted(set([m.strip() for m in members if isinstance(m, str) and m.strip()]))
    print("BUNDLE_MEMBERS:", ", ".join(members))
else:
    print("BUNDLE_MEMBERS: (none parsed) — open snapshot to confirm keys:")
    if snap.exists():
        d = json.loads(snap.read_text(encoding="utf-8"))
        if isinstance(d, dict):
            print("SNAPSHOT_TOP_KEYS:", ", ".join(sorted([str(k) for k in d.keys()])))
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
