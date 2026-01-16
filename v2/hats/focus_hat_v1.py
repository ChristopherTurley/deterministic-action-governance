from __future__ import annotations

from typing import Any, Dict, List, Optional

from v2.hats.hat_interface import HatDecision, HatInterface, HatOutcome, stable_fingerprint


class FocusHatV1(HatInterface):
    """
    Focus Hat v1 (CANONICAL, TEST-DRIVEN)

    Non-executing governance:
    - validates context freshness (TTL)
    - enforces task/minutes caps
    - allows on happy path
    - requires recommit on drift between proposed and commit payloads
    """

    name: str = "FOCUS_HAT_V1"

    # Exact reason strings expected by tests
    REASON_CTX_MISSING_PREFIX = "context_missing_required_key:"
    REASON_PROP_MISSING_PREFIX = "proposal_missing_required_key:"
    REASON_CTX_STALE = "context_stale_ttl_exceeded"
    REASON_TASK_EXCEEDS_CAP = "focus_task_count_exceeds_cap"
    REASON_MINUTES_EXCEEDS_CAP = "focus_planned_minutes_exceeds_cap"
    REASON_MINUTES_EXCEEDS_REMAINING = "focus_planned_minutes_exceeds_remaining"
    REASON_RECOMMIT_PREFIX = "proposal_drift_requires_recommit:"

    def context_keys_consumed(self) -> List[str]:
        # Declare what we read (audit clarity)
        return [
            "focus_mode",
            "context_as_of_ts",
            "context_ttl_seconds",
            "task_count_cap",
            "tasks_remaining",
            "minutes_cap",
            "minutes_remaining",
        ]

    def proposal_required_keys(self) -> List[str]:
        # planned_minutes is optional; tests include paths with and without it
        return ["task_count", "now_ts"]

    def _missing_context_key(self, ctx: Dict[str, Any]) -> Optional[str]:
        for k in self.context_keys_consumed():
            if k not in ctx:
                return k
        return None

    def _missing_proposal_key(self, proposal: Dict[str, Any]) -> Optional[str]:
        for k in self.proposal_required_keys():
            if k not in proposal:
                return k
        return None

    def _is_stale(self, ctx: Dict[str, Any], now_ts: Any) -> bool:
        try:
            age = float(now_ts) - float(ctx["context_as_of_ts"])
            ttl = float(ctx["context_ttl_seconds"])
        except Exception:
            return True
        return age > ttl

    def decide_proposal(self, context: Dict[str, Any], proposal: Dict[str, Any]) -> HatOutcome:
        fp = stable_fingerprint(proposal)

        mk = self._missing_context_key(context)
        if mk is not None:
            return HatOutcome(
                hat_name=self.name,
                stage="PROPOSE",
                decision=HatDecision.REFUSE,
                reasons=[self.REASON_CTX_MISSING_PREFIX + mk],
                consumed_context_keys=self.context_keys_consumed(),
                proposal_fingerprint=fp,
            )

        pk = self._missing_proposal_key(proposal)
        if pk is not None:
            return HatOutcome(
                hat_name=self.name,
                stage="PROPOSE",
                decision=HatDecision.REFUSE,
                reasons=[self.REASON_PROP_MISSING_PREFIX + pk],
                consumed_context_keys=self.context_keys_consumed(),
                proposal_fingerprint=fp,
            )

        if self._is_stale(context, proposal.get("now_ts")):
            return HatOutcome(
                hat_name=self.name,
                stage="PROPOSE",
                decision=HatDecision.REFUSE,
                reasons=[self.REASON_CTX_STALE],
                consumed_context_keys=self.context_keys_consumed(),
                proposal_fingerprint=fp,
            )

        # Task cap enforcement
        try:
            task_count = int(proposal.get("task_count"))
            cap = int(context.get("task_count_cap"))
            remaining = int(context.get("tasks_remaining"))
        except Exception:
            # Fail closed if typing is bad
            return HatOutcome(
                hat_name=self.name,
                stage="PROPOSE",
                decision=HatDecision.REFUSE,
                reasons=[self.REASON_TASK_EXCEEDS_CAP],
                consumed_context_keys=self.context_keys_consumed(),
                proposal_fingerprint=fp,
            )

        if task_count > cap or task_count > remaining:
            return HatOutcome(
                hat_name=self.name,
                stage="PROPOSE",
                decision=HatDecision.REFUSE,
                reasons=[self.REASON_TASK_EXCEEDS_CAP],
                consumed_context_keys=self.context_keys_consumed(),
                proposal_fingerprint=fp,
            )

        # Minutes enforcement (optional)
        if "planned_minutes" in proposal and proposal.get("planned_minutes") is not None:
            try:
                planned = int(proposal.get("planned_minutes"))
                mcap = int(context.get("minutes_cap"))
                mrem = int(context.get("minutes_remaining"))
            except Exception:
                return HatOutcome(
                    hat_name=self.name,
                    stage="PROPOSE",
                    decision=HatDecision.REFUSE,
                    reasons=[self.REASON_MINUTES_EXCEEDS_CAP],
                    consumed_context_keys=self.context_keys_consumed(),
                    proposal_fingerprint=fp,
                )

            if planned > mcap:
                return HatOutcome(
                    hat_name=self.name,
                    stage="PROPOSE",
                    decision=HatDecision.REFUSE,
                    reasons=[self.REASON_MINUTES_EXCEEDS_CAP],
                    consumed_context_keys=self.context_keys_consumed(),
                    proposal_fingerprint=fp,
                )

            if planned > mrem:
                return HatOutcome(
                    hat_name=self.name,
                    stage="PROPOSE",
                    decision=HatDecision.REFUSE,
                    reasons=[self.REASON_MINUTES_EXCEEDS_REMAINING],
                    consumed_context_keys=self.context_keys_consumed(),
                    proposal_fingerprint=fp,
                )

        # Happy path
        return HatOutcome(
            hat_name=self.name,
            stage="PROPOSE",
            decision=HatDecision.ALLOW,
            reasons=[],
            consumed_context_keys=self.context_keys_consumed(),
            proposal_fingerprint=fp,
        )

    def decide_commit(
        self,
        context: Dict[str, Any],
        proposed_proposal: Dict[str, Any],
        commit_proposal: Dict[str, Any],
    ) -> HatOutcome:
        # First, ensure the originally proposed payload is still admissible.
        # (Commit gating is about drift, not re-optimizing.)
        proposed_out = self.decide_proposal(context, proposed_proposal)
        if proposed_out.decision != HatDecision.ALLOW:
            return HatOutcome(
                hat_name=self.name,
                stage="COMMIT",
                decision=HatDecision.REFUSE,
                reasons=list(proposed_out.reasons),
                consumed_context_keys=self.context_keys_consumed(),
                proposal_fingerprint=stable_fingerprint(commit_proposal),
            )

        # Drift detection (ignore now_ts drift; allow clock movement)
        drift_fields = ["task_count", "planned_minutes"]
        for k in drift_fields:
            if commit_proposal.get(k) != proposed_proposal.get(k):
                return HatOutcome(
                    hat_name=self.name,
                    stage="COMMIT",
                    decision=HatDecision.REQUIRE_RECOMMIT,
                    reasons=[self.REASON_RECOMMIT_PREFIX + str(k)],
                    consumed_context_keys=self.context_keys_consumed(),
                    proposal_fingerprint=stable_fingerprint(commit_proposal),
                )

        # If commit equals proposed (for drift fields) and constraints were ok, allow.
        return HatOutcome(
            hat_name=self.name,
            stage="COMMIT",
            decision=HatDecision.ALLOW,
            reasons=[],
            consumed_context_keys=self.context_keys_consumed(),
            proposal_fingerprint=stable_fingerprint(commit_proposal),
        )
