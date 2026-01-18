from __future__ import annotations
from pathlib import Path

REQUIRED = [
  "README.md",
  "v2/docs/public/COMMERCIAL_BUNDLE_V1.md",
  "v2/device_b/MANIFEST.json",
  "v2/device_b/verify_all.py",
  "v2/legal/VERA_COMMERCIAL_BUNDLE_V1_LICENSE.md",
  "v2/legal/PROCUREMENT_RIDER_ONE_PAGER.md",
  "v2/sales/COMPLIANCE_GRADE_SALES_BRIEF_V1.md",
  "v2/sales/PROCUREMENT_COVER_MEMO_V1.md",
  "v2/bundles/commercial_bundle_v1/BUNDLE_SNAPSHOT.json",
]

FORBIDDEN_DIR_NAMES = [
  "integrations",
  "connectors",
  "plugins",
  "runtime",
  "agent",
  "automation",
  "saas",
  "telemetry",
  "tracking",
]

def test_repo_structure_required_surfaces_present():
    for p in REQUIRED:
        assert Path(p).exists(), f"missing_required_surface: {p}"

def test_repo_structure_forbids_productization_dirs():
    # fail closed if someone adds suspicious top-level dirs later
    top = [p for p in Path(".").iterdir() if p.is_dir()]
    bad = [p.name for p in top if p.name.lower() in FORBIDDEN_DIR_NAMES]
    assert not bad, f"forbidden_top_level_dirs_present: {bad}"
