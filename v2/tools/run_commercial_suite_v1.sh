set -eu
REPO="/Users/cp/ai_screen_assistant"
cd "$REPO" || exit 1

if [ ! -d venv ]; then
  python3 -m venv venv
fi
. venv/bin/activate

python -m pip install -U pip >/dev/null
python -m pip install -U pytest >/dev/null

export PYTHONPATH="."

# Commercial-only suite (locked). Do NOT run all of v2/tests.
python -m pytest -q \
  v2/tests/test_repo_structure_lock_v1.py \
  v2/tests/test_repo_commercial_only_lock_v1.py \
  v2/tests/test_repo_root_minimal_lock_v1.py \
  v2/tests/test_core_surface_lock_v1.py \
  v2/tests/test_device_b_artifacts_present.py \
  v2/tests/test_device_b_manifest_matches.py \
  v2/tests/test_commercial_bundle_v1_snapshot_locked.py \
  v2/tests/test_license_non_dilution_invariants.py \
  v2/tests/test_sales_brief_invariants.py \
  v2/tests/test_procurement_memo_invariants.py \
  v2/tests/test_coat_non_interference_v1.py \
  v2/tests/test_coat_no_advice_language_v1.py \
  v2/tests/test_coat_exports_single_render_decision_v1.py \
  v2/tests/test_coat_template_coverage_v1.py \
  v2/tests/test_start_here_present_v1.py
