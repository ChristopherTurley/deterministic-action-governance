from __future__ import annotations

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
    ok, err = validate_named("EngineOutput", out)
    if ok:
        return out
    # If schema validation itself is unavailable, still return deterministic object.
    return out


def run_engine_via_v1(inp: EngineInput) -> EngineOutput:
    """
    v2 boundary adapter (router-level):
    - Calls v1 route_text (deterministic)
    - Emits route_kind + meta-derived declared actions
    - Does NOT attempt to speak or execute side effects (runtime owns that)
    - Validates EngineOutput against v2/schema.json (fail closed)
    """
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
        if isinstance(target, int):
            actions.append({"type": "OPEN_LINK_INDEX", "payload": {"target": target}})
        else:
            actions.append({"type": "OPEN_LINK_INDEX", "payload": {"target": None}})

    followup_until_utc: Optional[str] = None  # runtime-owned

    # Minimal deterministic state delta for awake/mode only
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

    out = EngineOutput(
        route_kind=str(kind),
        speak_text="",
        actions=actions,
        state_delta=delta,
        mode_set=mode_set,
        followup_until_utc=followup_until_utc,
        debug={"meta": meta, "raw_len": len(raw)},
    )

    ok, err = validate_named("EngineOutput", out)
    if not ok:
        return _error_output("ERROR_SCHEMA_OUTPUT", err)

    return out
