from __future__ import annotations

from typing import Dict

# Month 8 Week 1: DEFAULT SAFE POLICY
# Nothing is allowed unless explicitly whitelisted.

DEFAULT_POLICY = {
    "allowed_actions": [],
}

def is_action_allowed(action_kind: str, policy: Dict | None = None) -> bool:
    if not action_kind:
        return False
    p = policy or DEFAULT_POLICY
    allowed = p.get("allowed_actions") or []
    return action_kind in allowed
