from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


import os
import tempfile
from typing import Any, Dict

from v2.pds_store import load_pds, save_pds


def _fail(msg: str) -> None:
    raise SystemExit("FAIL: " + msg)


def main() -> None:
    with tempfile.TemporaryDirectory() as d:
        os.environ["VERA_V2_PDS_DIR"] = d

        p0: Dict[str, Any] = {"awake": True, "actions_declared": [{"request_id": "r1"}]}
        fp = save_pds(p0, "2099-01-01")
        if not fp.exists():
            _fail("save_pds did not create file")

        p1 = load_pds("2099-01-01")
        if p1 != p0:
            _fail("loaded pds does not match saved pds")

        p2: Dict[str, Any] = {"awake": False, "outcomes": [{"status": "SUCCESS"}]}
        save_pds(p2, "2099-01-01")
        p3 = load_pds("2099-01-01")
        if p3 != p2:
            _fail("overwrite save/load mismatch")

    print("ALL MONTH3 PDS PERSIST SMOKE TESTS PASSED")


if __name__ == "__main__":
    main()
