from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Dict, List, Tuple


def _to_obj(x: Any) -> Any:
    if is_dataclass(x):
        return asdict(x)
    return x


def validate_engine_output(obj: Any) -> Tuple[bool, str]:
    """
    Minimal deterministic validator for EngineOutput contract.
    Enforces Trust without external dependencies.
    """
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
        # Allowed action types at router-boundary
        if a["type"] not in ["OPEN_LINK_INDEX", "NOOP"]:
            return False, f"actions[{i}].type not allowed: {a['type']}"

        if a["type"] == "OPEN_LINK_INDEX":
            if "target" not in a["payload"]:
                return False, "OPEN_LINK_INDEX payload must include target"

    if not isinstance(o["state_delta"], dict):
        return False, "state_delta must be dict"

    if o["mode_set"] not in ["IDLE", "INTAKE", "FOLLOWUP_OPEN", "FOLLOWUP_SCHEDULE"]:
        return False, "mode_set invalid"

    # followup_until_utc must be None or string (runtime-owned; usually None)
    if o["followup_until_utc"] is not None and not isinstance(o["followup_until_utc"], str):
        return False, "followup_until_utc must be None or string"

    if not isinstance(o["debug"], dict):
        return False, "debug must be dict"

    return True, ""


def validate_named(name: str, obj: Any) -> Tuple[bool, str]:
    if name == "EngineOutput":
        return validate_engine_output(obj)
    return False, f"unsupported validation target: {name}"
