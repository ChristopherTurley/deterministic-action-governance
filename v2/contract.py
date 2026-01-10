from __future__ import annotations

from typing import Any, Dict, List
import json

CONTRACT_VERSION = "v2_contract_v1"

def _jsonable(obj: Any) -> Any:
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, dict):
        return {k: _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_jsonable(v) for v in obj]
    to_dict = getattr(obj, "to_dict", None)
    if callable(to_dict):
        return _jsonable(to_dict())
    d = getattr(obj, "__dict__", None)
    if isinstance(d, dict):
        return _jsonable(d)
    try:
        return json.loads(json.dumps(obj, default=str))
    except Exception:
        return {"_repr": repr(obj)}

def _get_attr(obj: Any, keys: List[str], default=None):
    for k in keys:
        v = getattr(obj, k, None)
        if v is not None:
            return v
    return default

def to_contract_output(engine_out: Any, *, awake_fallback: bool) -> Dict[str, Any]:
    route_kind = _get_attr(engine_out, ["route_kind", "kind", "route", "route_name"], "") if engine_out is not None else ""
    route_kind = (route_kind or "").strip()

    awake = _get_attr(engine_out, ["awake"], None)
    if not isinstance(awake, bool):
        awake = bool(awake_fallback)

    receipts = _get_attr(engine_out, ["receipts", "receipt_list", "actions", "action_list", "planned_actions"], None)
    if not isinstance(receipts, list):
        one = _get_attr(engine_out, ["receipt", "action"], None)
        receipts = [one] if one is not None else []

    return {
        "version": CONTRACT_VERSION,
        "awake": awake,
        "route_kind": route_kind,
        "receipts": [_jsonable(r) for r in receipts],
    }
