from __future__ import annotations
from pathlib import Path

REQUIRED = [
  "artifact, not service",
  "offline, deterministic",
  "Vendor will NOT",
  "access customer systems",
  "access or process customer data",
  "Objective acceptance criteria",
  "Device-B verifier",
  "No ongoing support is implied",
  "AS IS",
  "does not guarantee regulatory approval",
]

def test_procurement_memo_contains_load_bearing_statements():
    p = Path("v2/sales/PROCUREMENT_COVER_MEMO_V1.md")
    assert p.exists(), "missing procurement cover memo"
    t = p.read_text(encoding="utf-8")
    for s in REQUIRED:
        assert s in t, f"procurement_memo_missing: {s}"
