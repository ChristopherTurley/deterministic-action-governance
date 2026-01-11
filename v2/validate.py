from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Dict, List, Tuple


def _to_obj(x: Any) -> Any:
    if is_dataclass(x):
        return asdict(x)
    return x


_ALLOWED_ACTIONS = {
    "NOOP",
    "OPEN_LINK_INDEX",
    "WEB_LOOKUP_QUERY",
    "SUGGESTION_ACCEPT",
    "SUGGESTION_REJECT",
    "SUGGESTION_DEFER",
    "SUGGESTION_REVISE",
    "PROPOSED_ACTION_COMMIT",
    "SPOTIFY_COMMAND",
    "STATE_SET_AWAKE",
    "ENTER_TASK_INTAKE",
    "TIME_READ",
    "PRIORITY_GET",
    "PRIORITY_SET",
}


def validate_engine_output(obj: Any) -> Tuple[bool, str]:
    o = _to_obj(obj)
    if not isinstance(o, dict):
        return False, "EngineOutput must be a dict-like object"

    required = ["route_kind", "speak_text", "actions", "state_delta", "mode_set", "followup_until_utc", "debug"]
    for k in required:
        if k not in o:
            return False, f"missing field: {k}"

    if not isinstance(o["route_kind"], str) or not o["route_kind"].strip():
        return False, "route_kind must be non-empty string"

    if not isinstance(o["speak_text"], str):
        return False, "speak_text must be string"

    if not isinstance(o["actions"], list):
        return False, "actions must be list"

    for i, a in enumerate(o["actions"]):
        if not isinstance(a, dict):
            return False, f"actions[{i}] must be dict"
        if "type" not in a or "payload" not in a:
            return False, f"actions[{i}] must include type and payload"
        if not isinstance(a["type"], str) or not a["type"].strip():
            return False, f"actions[{i}].type must be non-empty string"
        if not isinstance(a["payload"], dict):
            return False, f"actions[{i}].payload must be dict"

        t = a["type"]
        if t not in _ALLOWED_ACTIONS:
            return False, f"actions[{i}].type not allowed: {t!r}"

        p = a["payload"]

        if t == "OPEN_LINK_INDEX":
            if "target" not in p:
                return False, "OPEN_LINK_INDEX payload must include target"
            tgt = p.get("target", None)
            if tgt is not None and not isinstance(tgt, (int, str)):
                return False, "OPEN_LINK_INDEX target must be int, str, or None"

        if t == "WEB_LOOKUP_QUERY":
            q = p.get("query", None)
            if not isinstance(q, str) or not q.strip():
                return False, "WEB_LOOKUP_QUERY query must be non-empty string"


        if t == "SUGGESTION_ACCEPT":
            sid = p.get("suggestion_id", None)
            if not isinstance(sid, str) or not sid.strip():
                return False, "SUGGESTION_ACCEPT suggestion_id must be non-empty string"

        if t == "PROPOSED_ACTION_COMMIT":
            pid = p.get("proposal_id", None)
            if not isinstance(pid, str) or not pid.strip():
                return False, "PROPOSED_ACTION_COMMIT proposal_id must be non-empty string"
            return True, ""

        if t == "SPOTIFY_COMMAND":
            cmd = p.get("cmd", None)
            if not isinstance(cmd, str) or not cmd.strip():
                return False, "SPOTIFY_COMMAND cmd must be non-empty string"
            q = p.get("query", None)
            if q is not None and not isinstance(q, str):
                return False, "SPOTIFY_COMMAND query must be string or None"

        if t == "STATE_SET_AWAKE":
            if "awake" not in p or not isinstance(p.get("awake"), bool):
                return False, "STATE_SET_AWAKE awake must be bool"


        if t == "TIME_READ":
            # Read-only: payload may be empty dict
            pass

        if t == "PRIORITY_GET":
            # Read-only: payload may be empty dict
            pass

        if t == "PRIORITY_SET":
            # State change: allow item/priority to be present or omitted; payload must be dict (already enforced)
            item = p.get("item", None)
            pr = p.get("priority", None)
            if item is not None and not isinstance(item, (str, int)):
                return False, "PRIORITY_SET item must be str, int, or None"
            if pr is not None and not isinstance(pr, (str, int)):
                return False, "PRIORITY_SET priority must be str, int, or None"
        if t == "ENTER_TASK_INTAKE":
            if "enabled" not in p or not isinstance(p.get("enabled"), bool):
                return False, "ENTER_TASK_INTAKE enabled must be bool"

    if not isinstance(o["state_delta"], dict):
        return False, "state_delta must be dict"

    if o["mode_set"] not in ["IDLE", "INTAKE", "FOLLOWUP_OPEN", "FOLLOWUP_SCHEDULE"]:
        return False, "mode_set invalid"

    if o["followup_until_utc"] is not None and not isinstance(o["followup_until_utc"], str):
        return False, "followup_until_utc must be None or string"

    if not isinstance(o["debug"], dict):
        return False, "debug must be dict"

    return True, ""



def validate_named(name: str, obj: Any) -> Tuple[bool, str]:
    if name == "EngineOutput":
        return validate_engine_output(obj)
    return False, f"unsupported validation target: {name}"
