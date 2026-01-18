from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

ROOT = Path(".").resolve()
MANIFEST = Path("v2/device_b/MANIFEST.json")

def _sha256_file(p: Path) -> str:
    h = sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def test_device_b_manifest_hashes_match_repo_files():
    assert MANIFEST.exists()
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    expected = data.get("sha256", {})
    assert expected, "manifest empty"

    for rel, exp in expected.items():
        p = ROOT / rel
        assert p.exists(), f"manifest file missing from repo: {rel}"
        got = _sha256_file(p)
        assert got == exp, f"hash mismatch for {rel}"
