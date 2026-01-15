from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VEC_PATH = ROOT / "v2" / "tests" / "test_vectors.json"

sys.path.insert(0, str(ROOT))

from v2.engine_adapter import EngineInput, run_engine_via_v1
from v2.validate import validate_named

KIND_ALLOWLIST = {
    "ASLEEP_IGNORE",
    "LLM_FALLBACK",
    "MISSION",
    "NUDGE_WAKE",
    "OPEN_LINK",
    "PRIORITY_GET",
    "PRIORITY_SET",
    "SCREEN_SUMMARY",
    "SLEEP",
    "SPOTIFY",
    "START_DAY",
    "TIME",
    "WAKE",
    "WEB_LOOKUP",
}


def _fail(msg: str) -> None:
    print("FAIL:", msg)
    sys.exit(1)


def _ok(msg: str) -> None:
    print("OK:", msg)


def _subset_match(expected: dict, actual: dict) -> bool:
    for k, v in expected.items():
        if k not in actual:
            return False
        if isinstance(v, dict) and isinstance(actual.get(k), dict):
            if not _subset_match(v, actual.get(k)):
                return False
        else:
            if actual.get(k) != v:
                return False
    return True


def main() -> None:
    data = json.loads(VEC_PATH.read_text(encoding="utf-8"))
    cases = data.get("cases", [])
    if not isinstance(cases, list) or len(cases) != 20:
        _fail("expected exactly 20 cases")

    for c in cases:
        cid = c.get("id", "unknown")
        inp = c.get("input", {})
        asserts = c.get("assert", {})

        out = run_engine_via_v1(
            EngineInput(
                raw_text=inp.get("raw_text", ""),
                awake=bool(inp.get("awake", True)),
                wake_required=bool(inp.get("wake_required", True)),
                priority_enabled=bool(inp.get("priority_enabled", True)),
            )
        )

        ok, err = validate_named("EngineOutput", out)
        if not ok:
            _fail(f"{cid}: output failed validation: {err}")

        # Allow explicit ERROR_* codes, otherwise enforce allowlist.
        if isinstance(out.route_kind, str) and out.route_kind.startswith("ERROR_"):
            pass
        else:
            if out.route_kind not in KIND_ALLOWLIST:
                _fail(f"{cid}: route_kind not in allowlist: {out.route_kind!r}")

        rk_eq = asserts.get("route_kind_equals", None)
        if isinstance(rk_eq, str):
            if out.route_kind != rk_eq:
                _fail(f"{cid}: route_kind expected {rk_eq!r}, got {out.route_kind!r}")

        want_actions = asserts.get("actions_include", None)
        if isinstance(want_actions, list) and want_actions:
            have = out.actions or []
            for w in want_actions:
                matched = False
                for a in have:
                    if isinstance(a, dict) and _subset_match(w, a):
                        matched = True
                        break
                if not matched:
                    _fail(f"{cid}: missing action subset {w}. Have: {have}")

        _ok(f"{cid} route_kind={out.route_kind!r}")

    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
