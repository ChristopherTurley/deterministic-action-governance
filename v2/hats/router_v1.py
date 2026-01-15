from __future__ import annotations

from typing import Any, Dict, List, Tuple

from v2.hats.hat_interface import HatDecision
from v2.hats.registry import get_hat, list_hats


def route_proposal(hat_name: str, ctx: Dict[str, Any], proposal: Dict[str, Any]) -> Dict[str, Any]:
    hat = get_hat(hat_name)
    if hat is None:
        return {
            "type": "HAT_DECISION",
            "hat": (hat_name or "").strip().upper(),
            "stage": "PROPOSE",
            "decision": HatDecision.REFUSE.value,
            "reasons": ["unknown_hat:" + (hat_name or "").strip().upper()],
            "consumed_context_keys": [],
            "proposal_fingerprint": "UNKNOWN_HAT",
            "known_hats": list_hats(),
        }

    out = hat.decide_proposal(ctx, proposal)
    e = out.to_ledger_event()
    return e


def route_commit(hat_name: str, ctx: Dict[str, Any], proposed: Dict[str, Any], commit: Dict[str, Any]) -> Dict[str, Any]:
    hat = get_hat(hat_name)
    if hat is None:
        return {
            "type": "HAT_DECISION",
            "hat": (hat_name or "").strip().upper(),
            "stage": "COMMIT",
            "decision": HatDecision.REFUSE.value,
            "reasons": ["unknown_hat:" + (hat_name or "").strip().upper()],
            "consumed_context_keys": [],
            "proposal_fingerprint": "UNKNOWN_HAT",
            "known_hats": list_hats(),
        }

    out = hat.decide_commit(ctx, proposed, commit)
    e = out.to_ledger_event()
    return e
