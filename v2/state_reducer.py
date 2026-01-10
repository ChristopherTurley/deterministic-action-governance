from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class ReduceResult:
    next_state: Dict[str, Any]
    delta: Dict[str, Any]


def _clamp_int(x: Any, lo: int, hi: int, default: int) -> int:
    try:
        v = int(x)
    except Exception:
        return default
    if v < lo:
        return lo
    if v > hi:
        return hi
    return v


def _as_list(x: Any) -> List[Any]:
    return x if isinstance(x, list) else []


def reduce_pds(state: Dict[str, Any], delta: Dict[str, Any]) -> ReduceResult:
    """
    Month 2 Step 2 reducer (deterministic, conservative):
    - Still a shallow merge for unknown keys
    - Adds normalized directional fields:
      - commitments/dependencies/blockers: always lists
      - momentum: always object with score/reasons/updated_utc
    - Hard guardrails: never mutates unknown nested shapes; only normalizes when safe
    """
    if state is None:
        state = {}
    if delta is None:
        delta = {}

    next_state = dict(state)
    out_delta: Dict[str, Any] = {}

    for k, v in delta.items():
        next_state[k] = v
        out_delta[k] = v

    if "commitments" in next_state:
        next_state["commitments"] = _as_list(next_state.get("commitments"))
        out_delta["commitments"] = next_state["commitments"]

    if "dependencies" in next_state:
        next_state["dependencies"] = _as_list(next_state.get("dependencies"))
        out_delta["dependencies"] = next_state["dependencies"]

    if "blockers" in next_state:
        next_state["blockers"] = _as_list(next_state.get("blockers"))
        out_delta["blockers"] = next_state["blockers"]

    if "momentum" in next_state:
        m = next_state.get("momentum")
        if not isinstance(m, dict):
            m = {}
        m2 = {
            "score": _clamp_int(m.get("score"), 0, 100, 50),
            "reasons": _as_list(m.get("reasons")),
            "updated_utc": m.get("updated_utc", None),
        }
        next_state["momentum"] = m2
        out_delta["momentum"] = m2

    return ReduceResult(next_state=next_state, delta=out_delta)

def _receipt_type(receipt_or_rr: Any) -> str:
    if receipt_or_rr is None:
        return ""
    if isinstance(receipt_or_rr, dict):
        t = receipt_or_rr.get("type") or receipt_or_rr.get("kind") or receipt_or_rr.get("route_kind") or ""
        return str(t).strip().upper()
    for k in ("type", "kind", "route_kind"):
        v = getattr(receipt_or_rr, k, None)
        if isinstance(v, str) and v.strip():
            return v.strip().upper()
    return ""

def reduce_state(state: Any, receipt_or_rr: Any) -> Dict[str, Any]:
    """
    Month 6 Week 1: canonical reducer entry.
    Conservative + deterministic:
    - Never mutates input
    - Only applies whitelisted deltas (awake transitions) inferred from receipt type/kind
    - Falls back to no-op delta
    """
    s0: Dict[str, Any]
    if isinstance(state, dict):
        s0 = dict(state)
    else:
        d = getattr(state, "__dict__", None)
        s0 = dict(d) if isinstance(d, dict) else {}

    t = _receipt_type(receipt_or_rr)

    delta: Dict[str, Any] = {}
    if t == "WAKE":
        delta["awake"] = True
    elif t == "SLEEP":
        delta["awake"] = False

    rr = reduce_pds(s0, delta)
    return rr.next_state

