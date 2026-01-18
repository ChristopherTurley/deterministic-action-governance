#!/usr/bin/env python3
from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "v2" / "device_b" / "MANIFEST.json"

FILES = [
    # bundle packaging docs
    "v2/docs/public/COMMERCIAL_BUNDLE_V1.md",

    # trading hat frozen surfaces
    "v2/hats/trading_hat_v1.py",
    "v2/docs/hats/TRADING_HAT_V1.md",
    "v2/reference/trading_hat_v1/scenarios.json",
    "v2/reference/trading_hat_v1/reference_receipts.json",
    "v2/tools/run_trading_hat_v1.py",
    "v2/tests/test_trading_hat_v1_freeze.py",

    # executive hat frozen surfaces
    "v2/hats/executive_hat_v1.py",
    "v2/docs/hats/EXECUTIVE_HAT_V1.md",
    "v2/reference/executive_hat_v1/scenarios.json",
    "v2/reference/executive_hat_v1/reference_receipts.json",
    "v2/tools/run_executive_hat_v1.py",
    "v2/tests/test_executive_hat_v1_freeze.py",

    # ops incident hat frozen surfaces
    "v2/hats/ops_incident_hat_v1.py",
    "v2/docs/hats/OPS_INCIDENT_HAT_V1.md",
    "v2/reference/ops_incident_hat_v1/scenarios.json",
    "v2/reference/ops_incident_hat_v1/reference_receipts.json",
    "v2/tools/run_ops_incident_hat_v1.py",
    "v2/tests/test_ops_incident_hat_v1_freeze.py",

    # device-b tools
    "v2/device_b/verify_all.py",
]

def _sha256_file(p: Path) -> str:
    h = sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    sha = {}
    missing = []
    for rel in FILES:
        p = ROOT / rel
        if not p.exists():
            missing.append(rel)
            continue
        sha[rel] = _sha256_file(p)

    if missing:
        raise SystemExit("FAIL: missing files for manifest: " + ", ".join(missing))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"sha256": sha}, indent=2, sort_keys=True), encoding="utf-8")
    print(str(OUT))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
