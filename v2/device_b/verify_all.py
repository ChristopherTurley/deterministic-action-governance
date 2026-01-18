#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Device-B contract:
# - offline friendly
# - deterministic replay
# - fail-closed on mismatch

TOOLS = [
    ("EDUCATION_HAT_V1", "v2/tools/run_education_hat_v1.py", "v2/reference/education_hat_v1/reference_receipts.json"),
    ("HEALTHCARE_HAT_V1", "v2/tools/run_healthcare_hat_v1.py", "v2/reference/healthcare_hat_v1/reference_receipts.json"),
    ("TRADING_HAT_V1", "v2/tools/run_trading_hat_v1.py", "v2/reference/trading_hat_v1/reference_receipts.json"),
    ("EXECUTIVE_HAT_V1", "v2/tools/run_executive_hat_v1.py", "v2/reference/executive_hat_v1/reference_receipts.json"),
    ("OPS_INCIDENT_HAT_V1", "v2/tools/run_ops_incident_hat_v1.py", "v2/reference/ops_incident_hat_v1/reference_receipts.json"),
]

MANIFEST = ROOT / "v2" / "device_b" / "MANIFEST.json"

def _sha256_file(p: Path) -> str:
    h = sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def _run(py: str, script_rel: str) -> None:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)
    subprocess.check_call([py, str(ROOT / script_rel)], cwd=str(ROOT), env=env)

def main() -> int:
    py = sys.executable

    # 1) Run replays (deterministic generation must not error)
    for hat_id, tool, out_path in TOOLS:
        _run(py, tool)
        if not (ROOT / out_path).exists():
            raise SystemExit(f"FAIL: missing output for {hat_id}: {out_path}")

    # 2) Hash critical surfaces and compare to manifest (fail-closed)
    if not MANIFEST.exists():
        raise SystemExit("FAIL: MANIFEST.json missing (must be generated in repo, committed, and used for verification)")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    expected = manifest.get("sha256", {})
    bad = []

    for rel, exp in expected.items():
        p = ROOT / rel
        if not p.exists():
            bad.append({"file": rel, "problem": "missing"})
            continue
        got = _sha256_file(p)
        if got != exp:
            bad.append({"file": rel, "problem": "hash_mismatch", "expected": exp, "got": got})

    if bad:
        print("DEVICE_B_VERIFY_FAIL")
        print(json.dumps({"mismatches": bad}, indent=2, sort_keys=True))
        return 2

    print("DEVICE_B_VERIFY_OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
