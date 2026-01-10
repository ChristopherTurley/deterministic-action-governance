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

def apply_contract(engine_out: Any, *, awake_fallback: bool) -> Any:
    c = to_contract_output(engine_out, awake_fallback=awake_fallback)

    rk = (c.get("route_kind") or "").strip().upper()
    if rk == "WAKE":
        c["awake"] = True
    elif rk == "SLEEP":
        c["awake"] = False

    if isinstance(engine_out, dict):
        engine_out.update(c)
        engine_out["contract"] = c
        return engine_out

    for k, v in c.items():
        try:
            setattr(engine_out, k, v)
        except Exception:
            pass

    try:
        setattr(engine_out, "contract", c)
    except Exception:
        pass

    return engine_out

# === MONTH6W3_CANONICAL_CONTRACT ===

def _m6w3_normalize_receipt(r):
    if r is None:
        return {"type": "UNKNOWN", "payload": {}}
    if isinstance(r, dict):
        t = r.get("type") or r.get("kind") or r.get("route_kind") or "UNKNOWN"
        t = str(t).strip() or "UNKNOWN"
        payload = r.get("payload")
        if not isinstance(payload, dict):
            payload = r.get("data") if isinstance(r.get("data"), dict) else {}
        return {"type": t, "payload": payload}
    t = getattr(r, "type", None) or getattr(r, "kind", None) or getattr(r, "route_kind", None) or "UNKNOWN"
    t = str(t).strip() or "UNKNOWN"
    payload = getattr(r, "payload", None)
    if not isinstance(payload, dict):
        payload = {}
    return {"type": t, "payload": payload}

def _m6w3_canonicalize_contract_output(c):
    if not isinstance(c, dict):
        c = {"route_kind": str(c), "receipts": [], "actions": []}

    rk = c.get("route_kind")
    if not isinstance(rk, str) or not rk.strip():
        c["route_kind"] = "UNKNOWN"

    receipts = c.get("receipts")
    actions = c.get("actions")

    if not isinstance(receipts, list):
        receipts = []
    if not isinstance(actions, list):
        actions = []

    c["receipts"] = [_m6w3_normalize_receipt(r) for r in receipts]
    c["actions"] = [a if isinstance(a, dict) else {"_repr": repr(a)} for a in actions]
    return c

# Wrap to_contract_output so every internal return path becomes canonical.
_to_contract_output_impl_m6w3 = to_contract_output

def to_contract_output(*args, **kwargs):
    c = _to_contract_output_impl_m6w3(*args, **kwargs)
    return _m6w3_canonicalize_contract_output(c)

