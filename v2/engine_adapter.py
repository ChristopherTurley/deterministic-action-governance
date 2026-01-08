from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from v2.state_reducer import reduce_pds
from v2.validate import validate_named


@dataclass(frozen=True)
class EngineInput:
    raw_text: str
    wake_required: bool = True
    priority_enabled: bool = True
    awake: bool = True
    timestamp_utc: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    pds: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class EngineOutput:
    route_kind: str
    speak_text: str
    actions: List[Dict[str, Any]]
    state_delta: Dict[str, Any]
    mode_set: str
    followup_until_utc: Optional[str]
    debug: Dict[str, Any]


def _error_output(code: str, detail: str) -> EngineOutput:
    out = EngineOutput(
        route_kind=code,
        speak_text="",
        actions=[{"type": "NOOP", "payload": {"error": detail}}],
        state_delta={},
        mode_set="IDLE",
        followup_until_utc=None,
        debug={"error": detail},
    )
    ok, _ = validate_named("EngineOutput", out)
    if ok:
        return out
    return out


def run_engine_via_v1(inp: EngineInput) -> EngineOutput:
    raw = (inp.raw_text or "").strip()

    try:
        import assistant.router.core as v1_core
    except Exception as e:
        return _error_output("ERROR_IMPORT_V1", repr(e))

    try:
        rr = v1_core.route_text(
            raw,
            wake_required=bool(inp.wake_required),
            priority_enabled=bool(inp.priority_enabled),
            awake=bool(inp.awake),
        )
    except Exception as e:
        return _error_output("ERROR_V1_ROUTE", repr(e))

    kind = getattr(rr, "kind", "") or "UNKNOWN"
    meta = getattr(rr, "meta", {}) or {}

    actions: List[Dict[str, Any]] = []

    if kind == "OPEN_LINK":
        target = meta.get("target", None)
        actions.append({"type": "OPEN_LINK_INDEX", "payload": {"target": target}})

    if kind == "WEB_LOOKUP":
        q = meta.get("query", None)
        if not isinstance(q, str) or not q.strip():
            q = (getattr(rr, "cleaned", "") or "").strip()
        actions.append({"type": "WEB_LOOKUP_QUERY", "payload": {"query": str(q)}})

    if kind == "SPOTIFY":
        cmd = meta.get("cmd", "")
        q = meta.get("query", None)
        payload: Dict[str, Any] = {"cmd": str(cmd)}
        if q is not None:
            payload["query"] = str(q)
        actions.append({"type": "SPOTIFY_COMMAND", "payload": payload})

    if kind == "WAKE":
        actions.append({"type": "STATE_SET_AWAKE", "payload": {"awake": True}})

    if kind == "SLEEP":
        actions.append({"type": "STATE_SET_AWAKE", "payload": {"awake": False}})

    if kind == "START_DAY":
        actions.append({"type": "ENTER_TASK_INTAKE", "payload": {"enabled": True}})

    followup_until_utc: Optional[str] = None

    mode_set = "IDLE"

    if kind == "WAKE":
        delta = {"awake": True, "mode": mode_set}
    elif kind == "SLEEP":
        delta = {"awake": False, "mode": mode_set}
    else:
        delta = {"awake": bool(inp.awake), "mode": mode_set}

    try:
        _ = reduce_pds(inp.pds or {}, delta)
    except Exception:
        delta = {}

    debug = {"meta": meta, "raw_len": len(raw), "ts_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

    out = EngineOutput(
        route_kind=str(kind),
        speak_text="",
        actions=actions,
        state_delta=delta,
        mode_set=mode_set,
        followup_until_utc=followup_until_utc,
        debug=debug,
    )

    ok, err = validate_named("EngineOutput", out)
    if not ok:
        return _error_output("ERROR_SCHEMA_OUTPUT", err)

    return out
