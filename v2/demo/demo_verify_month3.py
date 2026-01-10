from __future__ import annotations

# Ensure repo root is importable when running this file directly.
import sys
from pathlib import Path as _Path
_repo_root = _Path(__file__).resolve().parents[2]
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

from assistant.runtime.app import VeraApp

from v2.engine_adapter import EngineInput, run_engine_via_v1
from v2.runtime_executor import execute_actions
from v2.accountability import apply_declared, apply_receipts
from v2.pds_store import load_pds, save_pds, pds_path


def _utc_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _today_local_ymd() -> str:
    return time.strftime("%Y-%m-%d", time.localtime())


def _debug_path() -> Path:
    fp = Path("v2") / "_pds" / "_debug" / (_today_local_ymd() + ".demo_verify.log")
    fp.parent.mkdir(parents=True, exist_ok=True)
    return fp


def _log(event: str, payload: Dict[str, Any]) -> None:
    fp = _debug_path()
    rec = {"utc": _utc_iso(), "event": event, "payload": payload}
    fp.write_text(fp.read_text(encoding="utf-8") + json.dumps(rec, ensure_ascii=False) + "\n", encoding="utf-8") if fp.exists() else fp.write_text(json.dumps(rec, ensure_ascii=False) + "\n", encoding="utf-8")


def _pretty(obj: Any) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True)

def _load_vectors() -> list:
    fp = Path("v2") / "tests" / "test_vectors.json"
    if not fp.exists():
        return []
    try:
        import json
        data = json.loads(fp.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            cases = data.get("cases", [])
            return cases if isinstance(cases, list) else []
        return []
    except Exception:
        return []
    try:
        import json
        data = json.loads(fp.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []





def _pick_case_for_route(vectors: list, route_kind: str) -> dict:
    """
    Deterministically choose a known-good CASE from v2/tests/test_vectors.json
    by matching assert.route_kind_equals == route_kind.
    Returns the whole case so we can reuse awake/wake_required/priority_enabled.
    """
    rk = (route_kind or "").strip().upper()
    for c in vectors:
        if not isinstance(c, dict):
            continue
        asserts = c.get("assert", {})
        if not isinstance(asserts, dict):
            continue
        eq = str(asserts.get("route_kind_equals", "") or "").strip().upper()
        if eq != rk:
            continue
        inp = c.get("input", {})
        if not isinstance(inp, dict):
            continue
        raw = inp.get("raw_text", "")
        if isinstance(raw, str) and raw.strip():
            return c
    return {}


def _mk_request_id(i: int) -> str:
    return f"demo-{_today_local_ymd()}-{i:02d}-{_utc_iso()}"


def _run_step(app: VeraApp, pds: Dict[str, Any], i: int, text: str, case_input: Dict[str, Any] | None = None) -> Tuple[Dict[str, Any], str, List[Dict[str, Any]], List[Dict[str, Any]]]:
    req = _mk_request_id(i)
    ci = case_input or {}
    raw_text = str(ci.get("raw_text", text) or text)
    awake = bool(ci.get("awake", bool(getattr(app.store.state, "awake", True))))
    wake_required = bool(ci.get("wake_required", True))
    priority_enabled = bool(ci.get("priority_enabled", True))

    inp = EngineInput(
        raw_text=raw_text,
        awake=awake,
        wake_required=wake_required,
        priority_enabled=priority_enabled,
        pds=pds,
        timestamp_utc=_utc_iso(),
    )
    out = run_engine_via_v1(inp)

    actions = out.actions or []
    _log("ENGINE_OUT", {"request_id": req, "raw": text, "route_kind": out.route_kind, "actions": actions})

    if actions:
        try:
            pds = apply_declared(pds, actions, request_id=req, route_kind=out.route_kind, ts_utc=_utc_iso())
        except TypeError:
            pds = apply_declared(pds, actions)

    primary_text = ""
    receipts: List[Dict[str, Any]] = []
    if actions:
        primary_text, receipts = execute_actions(app, req, actions)
        if receipts:
            pds = apply_receipts(pds, receipts)

    # Persist only when actions/receipts happened (contract)
    if actions or receipts:
        save_pds(pds)

    return pds, primary_text, actions, receipts


def main() -> int:
    # Use demo-specific PDS dir to avoid touching your daily state
    demo_dir = Path("v2") / "_pds" / "_demo"
    demo_dir.mkdir(parents=True, exist_ok=True)
    os.environ["VERA_V2_PDS_DIR"] = str(demo_dir.resolve())

    # Fresh demo PDS
    fp = pds_path(_today_local_ymd())
    if fp.exists():
        fp.unlink()

    print("=== VERA Month 3 Demo Verification ===")
    print("UTC:", _utc_iso())
    print("PDS_DIR:", str(demo_dir.resolve()))
    print("DEBUG_LOG:", str(_debug_path().resolve()))
    print("")

    app = VeraApp()  # v1 runtime app, used only as an execution surface for handlers
    pds = load_pds()
    vectors = _load_vectors()

    # Keep the web search demo query (it’s strong + readable), but everything else should be known-good vectors.
    # This makes the demo router-proof and stable across phrasing changes.
    vectors = _load_vectors()

    def _case_input(rk: str) -> dict:
        c = _pick_case_for_route(vectors, rk)
        inp = c.get("input", {}) if isinstance(c, dict) else {}
        return inp if isinstance(inp, dict) else {}

    steps = [
        ("Wake", _case_input("WAKE").get("raw_text", "hey vera"), _case_input("WAKE")),
        ("Web search", "search the web for pizza near me", None),
        ("Open link", _case_input("OPEN_LINK").get("raw_text", "open 1"), _case_input("OPEN_LINK")),
        ("Spotify", _case_input("SPOTIFY").get("raw_text", "spotify play lofi"), _case_input("SPOTIFY")),
        ("Start day", _case_input("START_DAY").get("raw_text", "start my day"), _case_input("START_DAY")),
        ("Time", _case_input("TIME").get("raw_text", "what time is it"), _case_input("TIME")),
        ("Priority get", _case_input("PRIORITY_GET").get("raw_text", "what are my priorities"), _case_input("PRIORITY_GET")),
        ("Sleep", _case_input("SLEEP").get("raw_text", "go to sleep"), _case_input("SLEEP")),
    ]
    for i, (label, text, case_input) in enumerate(steps, start=1):
        print(f"--- STEP {i:02d}: {label} ---")
        print("INPUT:", text)

        pds, primary_text, actions, receipts = _run_step(app, pds, i, text, case_input=case_input)

        print("DECLARED_ACTIONS:", _pretty(actions))
        print("RECEIPTS:", _pretty(receipts))

        if primary_text:
            print("OUTPUT_TEXT:", primary_text.strip())
        else:
            print("OUTPUT_TEXT:", "(none)")

        print("PDS_WRITTEN:", "yes" if (actions or receipts) else "no")
        print("")

    # Final snapshot
    fp = pds_path(_today_local_ymd())
    final = load_pds()
    print("=== FINAL PDS SNAPSHOT ===")
    print("PDS_PATH:", str(fp.resolve()))
    print(_pretty(final))
    print("=== END ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
