#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.." || exit 1
export PYTHONPATH="."

# Prefer venv python if activated; fallback to python3 if needed.
PYBIN="python"
command -v "$PYBIN" >/dev/null 2>&1 || PYBIN="python3"

# Only run the commercial bundle tests by filename patterns (nullglob avoids literal patterns).
shopt -s nullglob

FILES=(
  v2/tests/test_*hat*_freeze.py
  v2/tests/test_device_b_*.py
  v2/tests/test_reason_allowlists_v1.py
  v2/tests/test_commercial_bundle_v1_snapshot_locked.py
  v2/tests/test_license_*invariants*.py
  v2/tests/test_sales_brief_invariants.py
  v2/tests/test_procurement_memo_invariants.py
  v2/tests/test_repo_*lock*_v1.py
  v2/tests/test_core_surface_lock_v1.py
  v2/tests/test_coat_*v1.py
)

# Safety: ensure we actually matched something.
if [ "${#FILES[@]}" -eq 0 ]; then
  echo "ERROR: commercial suite matched zero tests; patterns may be wrong for this repo state."
  exit 2
fi

"$PYBIN" -m pytest -q "${FILES[@]}"
