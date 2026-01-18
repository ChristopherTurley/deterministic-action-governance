from __future__ import annotations

from pathlib import Path

def test_device_b_verifier_exists():
    assert Path("v2/device_b/verify_all.py").exists()
    assert Path("v2/device_b/generate_manifest.py").exists()
    assert Path("v2/device_b/MANIFEST.json").exists()

def test_commercial_bundle_doc_exists():
    assert Path("v2/docs/public/COMMERCIAL_BUNDLE_V1.md").exists()
