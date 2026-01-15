from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Dict, List


def _to_obj(x: Any) -> Any:
    if is_dataclass(x):
        return asdict(x)
    return x


def _as_list(x: Any) -> List[Any]:
    return x if isinstance(x, list) else []


def apply_declared(pds: Dict[str, Any], *args: Any) -> Dict[str, Any]:
    """
    Deterministic, fail-closed declared-action logger.

    Accepts any of these call styles (tolerant by design):
      1) apply_declared(pds, request_id: str, out: Any)
      2) apply_declared(pds, actions: list)
      3) apply_declared(pds, request_id: str, actions: list)

    Never throws. If inputs are unexpected, returns pds unchanged.
    """
    try:
        if pds is None:
            pds = {}
        p = dict(pds)

        request_id = None
        out_obj = None
        actions = None

        if len(args) == 2:
            request_id = args[0] if isinstance(args[0], str) else None
            if isinstance(args[1], list):
                actions = args[1]
            else:
                out_obj = args[1]
        elif len(args) == 1:
            if isinstance(args[0], list):
                actions = args[0]
            else:
                out_obj = args[0]
        elif len(args) >= 3:
            request_id = args[0] if isinstance(args[0], str) else None
            if isinstance(args[1], list):
                actions = args[1]
            else:
                out_obj = args[1]
            if actions is None and isinstance(args[2], list):
                actions = args[2]

        o = _to_obj(out_obj) if out_obj is not None else {}
        if actions is None:
            actions = _as_list(o.get('actions')) if isinstance(o, dict) else []
        else:
            actions = _as_list(actions)

        declared = _as_list(p.get('actions_declared'))
        entry = {
            'request_id': request_id,
            'route_kind': str(o.get('route_kind', '')) if isinstance(o, dict) else '',
            'actions': actions,
            'ts_utc': (o.get('debug') or {}).get('ts_utc', None) if isinstance(o, dict) else None,
        }
        declared.append(entry)
        p['actions_declared'] = declared
        return p
    except Exception:
        return dict(pds or {})

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
