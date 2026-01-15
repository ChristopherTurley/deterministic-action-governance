from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional
import hashlib
import json


class HatDecision(str, Enum):
    ALLOW = "ALLOW"
    REFUSE = "REFUSE"
    REQUIRE_RECOMMIT = "REQUIRE_RECOMMIT"


@dataclass(frozen=True)
class HatOutcome:
    hat_name: str
    decision: HatDecision
    reasons: List[str]
    consumed_context_keys: List[str]
    proposal_fingerprint: str
    stage: str  # "PROPOSE" or "COMMIT"

    def to_ledger_event(self) -> Dict[str, Any]:
        # Additive, audit-safe event. Caller chooses where/how to persist.
        return {
            "type": "HAT_DECISION",
            "hat": self.hat_name,
            "stage": self.stage,
            "decision": self.decision.value,
            "reasons": list(self.reasons),
            "consumed_context_keys": list(self.consumed_context_keys),
            "proposal_fingerprint": self.proposal_fingerprint,
        }


class HatInterface:
    """
    Minimal hat contract:
    - deterministic outcomes
    - fail-closed by default
    - pure evaluation (no side effects)
    """

    name: str = "UNNAMED_HAT"

    def context_keys_consumed(self) -> List[str]:
        raise NotImplementedError

    def proposal_required_keys(self) -> List[str]:
        raise NotImplementedError

    def decide_proposal(self, context: Dict[str, Any], proposal: Dict[str, Any]) -> HatOutcome:
        raise NotImplementedError

    def decide_commit(
        self,
        context: Dict[str, Any],
        proposed_proposal: Dict[str, Any],
        commit_proposal: Dict[str, Any],
    ) -> HatOutcome:
        raise NotImplementedError


def stable_fingerprint(obj: Dict[str, Any]) -> str:
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
