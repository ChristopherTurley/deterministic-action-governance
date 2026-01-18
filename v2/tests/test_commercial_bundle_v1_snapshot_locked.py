from __future__ import annotations

import hashlib
import json
from pathlib import Path


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def test_commercial_bundle_v1_snapshot_locked():
    snap = Path("v2/bundles/commercial_bundle_v1/BUNDLE_SNAPSHOT.json")
    assert snap.exists(), "missing bundle snapshot"

    data = json.loads(snap.read_text(encoding="utf-8"))
    assert data["bundle_id"] == "COMMERCIAL_BUNDLE_V1"
    assert data["bundle_hats"] == [
        "TRADING_HAT_V1",
        "EXECUTIVE_HAT_V1",
        "OPS_INCIDENT_HAT_V1",
        "HEALTHCARE_HAT_V1",
        "EDUCATION_HAT_V1",
    ]

    mpath = Path(data["device_b_manifest_path"])
    dpath = Path(data["commercial_bundle_doc_path"])
    assert mpath.exists(), "Device-B MANIFEST missing"
    assert dpath.exists(), "Commercial bundle doc missing"

    assert _sha256_file(mpath) == data["device_b_manifest_sha256"]
    assert _sha256_file(dpath) == data["commercial_bundle_doc_sha256"]
