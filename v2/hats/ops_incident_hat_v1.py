from __future__ import annotations
from typing import Any, Dict, List
from v2.hats.hat_interface import HatDecision, HatInterface, HatOutcome, stable_fingerprint

class OpsIncidentHatV1(HatInterface):
    name: str = "OPS_INCIDENT_HAT_V1"

    def context_keys_consumed(self) -> List[str]:
        return []

    def proposal_required_keys(self) -> List[str]:
        return []

    def decide_proposal(self, context: Dict[str, Any], proposal: Dict[str, Any]) -> HatOutcome:
        return HatOutcome(
            hat_name=self.name,
            stage="PROPOSE",
            decision=HatDecision.REFUSE,
            reasons=["INV_OPS_REQUIRES_EXPLICIT_COMMIT"],
            consumed_context_keys=self.context_keys_consumed(),
            proposal_fingerprint=stable_fingerprint(proposal),
        )

    def decide_commit(self, context: Dict[str, Any], proposed_proposal: Dict[str, Any], commit_proposal: Dict[str, Any]) -> HatOutcome:
        return HatOutcome(
            hat_name=self.name,
            stage="COMMIT",
            decision=HatDecision.REFUSE,
            reasons=["INV_OPS_REQUIRES_EXPLICIT_COMMIT"],
            consumed_context_keys=self.context_keys_consumed(),
            proposal_fingerprint=stable_fingerprint(commit_proposal),
        )
