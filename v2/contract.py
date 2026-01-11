from __future__ import annotations

from typing import Any, Dict, List
import json
import hashlib
CONTRACT_VERSION = "v2_contract_v1"
CONTEXT_VERSION = "context_v1"

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


def _normalize_context_v1(ctx: Any) -> Dict[str, Any]:
    if not isinstance(ctx, dict):
        return {}
    allowed = ("active_app", "local_date", "local_time", "screen_hint")
    out: Dict[str, Any] = {}
    for k in allowed:
        v = ctx.get(k, None)
        if v is None:
            continue
        out[k] = str(v)
    return out

def _extract_context_any(engine_out: Any) -> Dict[str, Any]:
    ctx = _get_attr(engine_out, ["context"], None)
    if isinstance(ctx, dict):
        return _normalize_context_v1(ctx)
    dbg = _get_attr(engine_out, ["debug"], None)
    if isinstance(dbg, dict):
        return _normalize_context_v1(dbg.get("context"))
    return {}
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
        "context_version": CONTEXT_VERSION,
        "context": _extract_context_any(engine_out),
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

# === MONTH7W2_ACTION_NORMALIZATION ===

def _m7w2_hash_id(obj) -> str:
    try:
        raw = json.dumps(obj, sort_keys=True, default=str).encode("utf-8")
    except Exception:
        raw = repr(obj).encode("utf-8")
    return hashlib.sha1(raw).hexdigest()[:12]

def _m7w2_normalize_action(a):
    if a is None:
        return {"id": _m7w2_hash_id("NONE"), "kind": "UNKNOWN", "payload": {}}
    if not isinstance(a, dict):
        return {"id": _m7w2_hash_id({"_repr": repr(a)}), "kind": "UNKNOWN", "payload": {}, "_repr": repr(a)}

    kind = a.get("kind") or a.get("action_kind") or a.get("type") or a.get("name") or "UNKNOWN"
    kind = str(kind).strip().upper() or "UNKNOWN"

    payload = a.get("payload")
    if not isinstance(payload, dict):
        payload = a.get("data") if isinstance(a.get("data"), dict) else {}

    aid = a.get("id") or a.get("action_id") or a.get("receipt_id") or a.get("event_id")
    aid = str(aid).strip() if isinstance(aid, str) else ""
    if not aid:
        # Stable ID derived from kind+payload only (deterministic)
        aid = _m7w2_hash_id({"kind": kind, "payload": payload})

    out = {"id": aid, "kind": kind, "payload": payload}
    # Keep any extra keys for debugging, but don't rely on them.
    if "_repr" in a:
        out["_repr"] = a["_repr"]
    return out

# Upgrade the existing canonicalizer to normalize actions too.
_m6w3_canonicalize_contract_output_prev = _m6w3_canonicalize_contract_output

def _m6w3_canonicalize_contract_output(c):
    c = _m6w3_canonicalize_contract_output_prev(c)
    actions = c.get("actions")
    if not isinstance(actions, list):
        actions = []
    c["actions"] = [_m7w2_normalize_action(a) for a in actions]
    return c

