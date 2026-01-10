from __future__ import annotations


def _normalize_web_query(raw: str) -> str:
    """
    WEB_QUERY_NORMALIZE_V1
    Deterministic, rules-only normalization for web lookup queries.
    Goal: turn messy transcripts into stable search queries without guessing.
    """
    q = (raw or "").strip()

    # Drop a leading "hey vera," if it survived upstream
    q = re.sub(r"^\s*hey\s+vera\s*,?\s*", "", q, flags=re.I)

    # Remove common intent prefixes
    q = re.sub(r"^\s*(search\s+(the\s+)?web\s+(for\s+)?)", "", q, flags=re.I)
    q = re.sub(r"^\s*(web\s*search\s+(for\s+)?)", "", q, flags=re.I)
    q = re.sub(r"^\s*(look\s*up\s+)", "", q, flags=re.I)
    q = re.sub(r"^\s*(lookup\s+)", "", q, flags=re.I)
    q = re.sub(r"^\s*(google\s+)", "", q, flags=re.I)
    q = re.sub(r"^\s*(find\s+)", "", q, flags=re.I)
    q = re.sub(r"^\s*(search\s+for\s+)", "", q, flags=re.I)

    # Normalize whitespace + punctuation edges
    q = q.replace("—", "-").replace("–", "-")
    q = re.sub(r"\s+", " ", q).strip(" \t\r\n.,!?;:")

    # --- Numeric normalization (targeted) ---
    # 9-11 / 9 11 / nine eleven -> 911 (ONLY in a context where it's likely a model number)
    q_low = q.lower()

    has_911_signal = bool(
        re.search(r"\b9\s*[- ]\s*11\b", q_low) or
        re.search(r"\b911\b", q_low) or
        re.search(r"\bnine\s+eleven\b", q_low)
    )

    if has_911_signal:
        q = re.sub(r"\b9\s*[- ]\s*11\b", "911", q, flags=re.I)
        q = re.sub(r"\bnine\s+eleven\b", "911", q, flags=re.I)

    # --- Transcript-noise correction (HIGH PRECISION only) ---
    # Only rewrite "portion/portia/porchia" -> "porsche" when 911 signal is present.
    if has_911_signal:
        q = re.sub(r"\bportion\b", "porsche", q, flags=re.I)
        q = re.sub(r"\bportia\b", "porsche", q, flags=re.I)
        q = re.sub(r"\bporchia\b", "porsche", q, flags=re.I)
        q = re.sub(r"\bporche\b", "porsche", q, flags=re.I)

    # Final cleanup
    q = re.sub(r"\s+", " ", q).strip()
    return q

import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from v2.state_reducer import reduce_pds
from v2.validate import validate_named

import re


def _normalize_web_search(raw: str) -> Dict[str, str]:
    """
    Deterministic v2-only normalization.
    Returns:
      {"mode": "PASS", "raw": raw}
      {"mode": "FOLLOWUP", "speak": "..."}
    """
    s = (raw or "").strip()
    low = re.sub(r"\s+", " ", s.lower()).strip()

    # Bare intent: requires a follow-up (no actions)
    if low in {"search the web", "search web", "search the internet", "search internet", "web search"}:
        return {"mode": "FOLLOWUP", "speak": "What would you like me to search the web for?"}

    # Normalize common phrases to a v1-friendly pattern that yields WEB_LOOKUP
    patterns = [
        r"^(search the web for)\s+(.+)$",
        r"^(search for)\s+(.+)$",
        r"^(look up)\s+(.+)$",
        r"^(lookup)\s+(.+)$",
        r"^(find)\s+(.+)$",
    ]
    for pat in patterns:
        m = re.match(pat, s.strip(), flags=re.IGNORECASE)
        if m:
            q = (m.group(2) or "").strip()
            if q:
                # v1 already supports "look up X"
                return {"mode": "DIRECT_WEB_LOOKUP", "query": q}

    return {"mode": "PASS", "raw": s}



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

    norm = _normalize_web_search(raw)
    if norm.get("mode") == "FOLLOWUP":
        out = EngineOutput(
            route_kind="WEB_LOOKUP_FOLLOWUP",
            speak_text=str(norm.get("speak") or ""),
            actions=[],
            state_delta={},
            mode_set="IDLE",
            followup_until_utc=None,
            debug={"normalized": True, "reason": "missing_query"},
        )
        ok, err = validate_named("EngineOutput", out)
        if not ok:
            return _error_output("ERROR_SCHEMA_OUTPUT", err)
        return out


    if norm.get("mode") == "DIRECT_WEB_LOOKUP":
        q = str(norm.get("query") or "").strip()
        out = EngineOutput(
            route_kind="WEB_LOOKUP",
            speak_text="",
            actions=[{"type": "WEB_LOOKUP_QUERY", "payload": {"query": _normalize_web_query(q)}}],
            state_delta={"awake": bool(inp.awake), "mode": "IDLE"},
            mode_set="IDLE",
            followup_until_utc=None,
            debug={"normalized": True, "direct": "WEB_LOOKUP_QUERY"},
        )
        ok, err = validate_named("EngineOutput", out)
        if not ok:
            return _error_output("ERROR_SCHEMA_OUTPUT", err)
        return out

    raw = str(norm.get("raw") or raw)


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
        actions.append({"type": "WEB_LOOKUP_QUERY", "payload": {"query": _normalize_web_query(str(q))}})

    if kind == "SPOTIFY":
        cmd = meta.get("cmd", "")
        q = meta.get("query", None)
        payload: Dict[str, Any] = {"cmd": str(cmd)}
        if q is not None:
            payload["query"] = str(q)
        actions.append({"type": "SPOTIFY_COMMAND", "payload": payload})

    rk = str(getattr(rr, "route_kind", "") or "").strip().upper()

    # TIME (read-only, but must be explicit for receipts)
    if rk == "TIME" or kind == "TIME":
        actions.append({"type": "TIME_READ", "payload": {}})

    # PRIORITY
    if rk == "PRIORITY_GET" or kind == "PRIORITY_GET":
        actions.append({"type": "PRIORITY_GET", "payload": {}})
    if rk == "PRIORITY_SET" or kind == "PRIORITY_SET":
        pld = meta if isinstance(meta, dict) else {}
        actions.append({"type": "PRIORITY_SET", "payload": pld})


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
