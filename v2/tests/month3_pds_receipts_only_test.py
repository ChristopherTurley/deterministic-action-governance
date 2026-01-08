from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from v2.pds_store import load_pds, save_pds
from v2.engine_adapter import EngineInput, run_engine_via_v1


def _fail(msg: str) -> None:
    raise SystemExit("FAIL: " + msg)


def main() -> None:
    with tempfile.TemporaryDirectory() as d:
        os.environ["VERA_V2_PDS_DIR"] = d

        base = {"date": "2099-01-01", "awake": True}
        save_pds(base, "2099-01-01")
        before = load_pds("2099-01-01")

        out = run_engine_via_v1(EngineInput(raw_text="hey vera, how are you", awake=True, wake_required=True))
        if out.actions:
            _fail("expected no actions for fallback-style utterance")

        after = load_pds("2099-01-01")
        if after != before:
            _fail("PDS changed on non-action utterance")

    print("ALL MONTH3 RECEIPTS-ONLY PDS TESTS PASSED")


if __name__ == "__main__":
    main()
