set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${0}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
cd "${REPO_ROOT}"
set -euo pipefail

REPO="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO" || exit 1

echo "=== COMMERCIAL SUITE v1 (CI-safe) ==="

echo "=== 0) LOCAL SETUP (venv + pytest; untracked; idempotent) ==="
if [ ! -d venv ]; then
  python3 -m venv venv
fi
. venv/bin/activate
python -m pip install -U pip >/dev/null
python -m pip install -U pytest >/dev/null
export PYTHONPATH="."

echo "=== 1) RUN LOCKED COMMERCIAL TESTS ==="
python -m pytest -q \
  v2/tests/test_start_here_present_v1.py \
  v2/tests/test_repo_commercial_only_lock_v1.py \
  v2/tests/test_repo_root_minimal_lock_v1.py \
  v2/tests/test_core_surface_lock_v1.py \
  v2/tests/test_reason_allowlists_v1.py \
  v2/tests/test_device_b_artifacts_present.py \
  v2/tests/test_device_b_manifest_matches.py \
  v2/tests/test_commercial_bundle_v1_snapshot_locked.py \
  v2/tests/test_license_non_dilution_invariants.py \
  v2/tests/test_sales_brief_invariants.py \
  v2/tests/test_procurement_memo_invariants.py
