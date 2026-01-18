from __future__ import annotations
from pathlib import Path

REQUIRED = [
  "governance-only reference artifact",
  "offline / air-gapped",
  "No SaaS",
  "No custom hats",
  "Objective acceptance criteria",
  "Device-B verifier",
  "Buyer pushbacks",
  "models change",
  "not legal indemnification",
  "verification, not real-time enforcement",
  "Why $100k",
]

def test_sales_brief_contains_load_bearing_sections():
    p = Path("v2/sales/COMPLIANCE_GRADE_SALES_BRIEF_V1.md")
    assert p.exists(), "missing sales brief"
    t = p.read_text(encoding="utf-8")
    for s in REQUIRED:
        assert s in t, f"sales_brief_missing: {s}"
