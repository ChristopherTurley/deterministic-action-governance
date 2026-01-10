
from __future__ import annotations
from v2.side_effect_policy import is_action_allowed

from typing import Any, Dict, List

def execute_actions(actions: Any, *, dry_run: bool = True) -> List[Dict[str, Any]]:
    """
    Canonical action executor entry point (Month 7 Week 1).
    Week 1 contract: callable + deterministic + safe.
    - Accepts actions (list-like)
    - Returns a list of dict receipts/results (empty for now)
    - Does NOT perform side effects (dry_run only semantics for Week 1)
    """
    if actions is None:
        actions_list: List[Any] = []
    elif isinstance(actions, list):
        actions_list = actions
    else:
        actions_list = [actions]

    # Normalize to dict-like action records; do not execute anything yet.
    norm: List[Dict[str, Any]] = []
    for a in actions_list:
        if isinstance(a, dict):
            norm.append(a)
        else:
            norm.append({"_repr": repr(a)})

    # Week 3: deterministic dry-run execution receipts (no side effects)
    out: List[Dict[str, Any]] = []
    for a in norm:
        out.append({
            "type": "ACTION_DRY_RUN",
            "payload": {
                "id": a.get("id"),
                "kind": a.get("kind"),
                "payload": a.get("payload") if isinstance(a.get("payload"), dict) else {},
            },
        })
    return out
