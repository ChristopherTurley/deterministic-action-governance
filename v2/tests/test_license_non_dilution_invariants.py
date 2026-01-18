from __future__ import annotations

from pathlib import Path

# This is a minimal “no dilution” invariant test.
# It does NOT provide legal advice.
# It ensures the license keeps the non-negotiable boundaries.

REQUIRED_PHRASES = [
    "governance-only reference artifact",
    "non-executing",
    "No support obligation",
    "AS IS",
    "not a guarantee of compliance",
    "Acceptance is satisfied if",
    "Device-B verifier",
    "Customer may not",
    "custom hats",
]

def test_license_contains_non_dilution_boundaries():
    p = Path("v2/legal/VERA_COMMERCIAL_BUNDLE_V1_LICENSE.md")
    assert p.exists(), "missing license file"
    t = p.read_text(encoding="utf-8")

    for phrase in REQUIRED_PHRASES:
        assert phrase in t, f"license_missing_required_phrase: {phrase}"
