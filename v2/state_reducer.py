from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Tuple


@dataclass(frozen=True)
class ReduceResult:
    next_state: Dict[str, Any]
    delta: Dict[str, Any]


def reduce_pds(state: Dict[str, Any], delta: Dict[str, Any]) -> ReduceResult:
    """
    Minimal reducer: applies a shallow merge.
    v2 will evolve this into strict, validated transitions.
    """
    if state is None:
        state = {}
    if delta is None:
        delta = {}
    next_state = dict(state)
    for k, v in delta.items():
        next_state[k] = v
    return ReduceResult(next_state=next_state, delta=delta)
