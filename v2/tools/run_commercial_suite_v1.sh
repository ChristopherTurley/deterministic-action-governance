set -euo pipefail

REPO="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO" || exit 1

export PYTHONPATH="."

# Run only the commercial-only locked tests (source of truth)
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
