set -eu
REPO="/Users/cp/ai_screen_assistant"
cd "$REPO" || exit 1

echo "============================================================"
echo "VERA v2 — COMMERCIAL BUNDLE v1 (START HERE)"
echo "============================================================"
echo

echo "COMMIT:"
git rev-parse --short HEAD 2>/dev/null || echo "UNKNOWN"
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
python - <<'PY2'
from v2.device_b.verify_all import main
main()
PY2
echo

echo "3) BUNDLE SNAPSHOT + MANIFEST"
echo "BUNDLE_SNAPSHOT: v2/bundles/commercial_bundle_v1/BUNDLE_SNAPSHOT.json"
echo "DEVICE_B_MANIFEST: v2/device_b/MANIFEST.json"
python - <<'PY3'
import json
from pathlib import Path
snap = Path("v2/bundles/commercial_bundle_v1/BUNDLE_SNAPSHOT.json")
d = json.loads(snap.read_text(encoding="utf-8"))
hats = d.get("bundle_hats") or d.get("hats") or []
if isinstance(hats, list) and hats:
    print("BUNDLE_MEMBERS:")
    for h in hats:
        if isinstance(h, str):
            print(" -", h)
        elif isinstance(h, dict):
            nm = h.get("id") or h.get("name") or h.get("hat") or str(h)
            print(" -", nm)
        else:
            print(" -", str(h))
else:
    print("BUNDLE_MEMBERS: (none parsed) — open snapshot to confirm keys:")
    print("SNAPSHOT_TOP_KEYS:", ", ".join(sorted(d.keys())))
PY3
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
