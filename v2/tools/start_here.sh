set -euo pipefail

REPO="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO" || exit 1

echo "============================================================"
echo "VERA v2 — COMMERCIAL BUNDLE v1 (START HERE)"
echo "============================================================"
echo

echo "REPO_HEAD:"
git rev-parse --short HEAD 2>/dev/null || echo "UNKNOWN"
echo

echo "BUNDLE_LOCK:"
git tag --points-at HEAD 2>/dev/null | grep -m1 'VERA_v2_COMMERCIAL_BUNDLE' || echo "(no bundle lock tag on this HEAD)"
echo

echo "0) LOCAL SETUP (venv + pytest; untracked; idempotent)"
if [ ! -d venv ]; then
  python3 -m venv venv
fi
. venv/bin/activate
python -m pip install -U pip >/dev/null
python -m pip install -U pytest >/dev/null
export PYTHONPATH="."
echo "OK: venv ready"
echo

echo "1) RUN COMMERCIAL SUITE (must be green)"
bash v2/tools/run_commercial_suite_v1.sh
echo

echo "2) DEVICE-B VERIFY (must be OK)"
python - <<'PYY'
from v2.device_b.verify_all import main
main()
PYY
echo

echo "3) BUNDLE SNAPSHOT + MANIFEST"
echo "BUNDLE_SNAPSHOT: v2/bundles/commercial_bundle_v1/BUNDLE_SNAPSHOT.json"
echo "DEVICE_B_MANIFEST: v2/device_b/MANIFEST.json"

python - <<'PYY'
import json
from pathlib import Path

snap = Path("v2/bundles/commercial_bundle_v1/BUNDLE_SNAPSHOT.json")
d = json.loads(snap.read_text(encoding="utf-8"))

hats = d.get("bundle_hats") or d.get("hats") or []
print("BUNDLE_MEMBERS:")
if isinstance(hats, list) and hats:
    for h in hats:
        if isinstance(h, str):
            print(" -", h)
        elif isinstance(h, dict):
            nm = h.get("id") or h.get("name") or h.get("hat") or str(h)
            print(" -", nm)
        else:
            print(" -", str(h))
else:
    print(" - (none parsed) — open snapshot to confirm keys:", ", ".join(sorted(d.keys())))
PYY
echo

echo "4) EVALUATOR DOCS (open these)"
echo " - v2/docs/public/REPO_MAP_COMMERCIAL_V1.md"
echo " - v2/docs/public/COMMERCIAL_BUNDLE_V1.md"
echo " - v2/sales/COMPLIANCE_GRADE_SALES_BRIEF_V1.md"
echo " - v2/sales/PROCUREMENT_COVER_MEMO_V1.md"
echo " - v2/legal/VERA_COMMERCIAL_BUNDLE_V1_LICENSE.md"
echo " - v2/legal/PROCUREMENT_RIDER_ONE_PAGER.md"
echo " - v2/legal/GARM_V1.md"
echo " - v2/docs/public/EVALUATOR_COURTESY.md"
echo
echo "DONE: If steps 1–2 are green/OK, the artifact is procurement-ready."

