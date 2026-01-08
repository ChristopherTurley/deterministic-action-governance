from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Dict, List


def _to_obj(x: Any) -> Any:
    if is_dataclass(x):
        return asdict(x)
    return x


def _as_list(x: Any) -> List[Any]:
    return x if isinstance(x, list) else []


def apply_declared(pds: Dict[str, Any], request_id: str, out: Any) -> Dict[str, Any]:
    o = _to_obj(out)
    if pds is None:
        pds = {}
    p = dict(pds)

    declared = _as_list(p.get("actions_declared"))
    entry = {
        "request_id": request_id,
        "route_kind": str(o.get("route_kind", "")),
        "actions": _as_list(o.get("actions")),
        "ts_utc": (o.get("debug") or {}).get("ts_utc", None) if isinstance(o.get("debug"), dict) else None,
    }
    declared.append(entry)
    p["actions_declared"] = declared

    return p


def apply_receipts(pds: Dict[str, Any], receipts: List[Dict[str, Any]]) -> Dict[str, Any]:
    if pds is None:
        pds = {}
    p = dict(pds)

    executed = _as_list(p.get("actions_executed"))
    outcomes = _as_list(p.get("outcomes"))

    for r in receipts or []:
        if not isinstance(r, dict):
            continue
        status = r.get("status")
        if status == "SUCCESS":
            executed.append(r)
        if status in ("SUCCESS", "FAILURE"):
            outcomes.append(
                {
                    "request_id": r.get("request_id"),
                    "action_type": r.get("action_type"),
                    "status": status,
                    "artifact": r.get("artifact", None),
                    "error": r.get("error", None),
                    "executed_at_utc": r.get("executed_at_utc", None),
                }
            )

    p["actions_executed"] = executed
    p["outcomes"] = outcomes
    return p
