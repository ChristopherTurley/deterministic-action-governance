from __future__ import annotations

from typing import Any, Dict, List, Tuple
from .hat_interface import HatDecision, HatInterface, HatOutcome, stable_fingerprint


class TradingHatV1(HatInterface):
    """
    Trading Hat v1: mechanical governance only.
    - No strategy generation
    - No prediction
    - Deterministic allow/refuse/recommit
    """

    name: str = "TRADING_HAT_V1"

    # Context keys (read-only, declared by operator/system)
    _context_keys: List[str] = [
        "instrument",
        "time_of_day",
        "volatility_state",
        "liquidity_state",
        "max_daily_loss",
        "daily_loss",
        "trades_taken_today",
        "trade_count_cap",
        "context_as_of_ts",
        "context_ttl_seconds",
    ]

    # Proposal requirements (operator-provided)
    _proposal_required: List[str] = [
        "entry_intent",
        "size",
        "max_loss",
        "invalidation",
        "time_constraint",
        "now_ts",
        "instrument",
    ]

    def context_keys_consumed(self) -> List[str]:
        return list(self._context_keys)

    def proposal_required_keys(self) -> List[str]:
        return list(self._proposal_required)

    def _missing_keys(self, src: Dict[str, Any], keys: List[str]) -> List[str]:
        missing: List[str] = []
        for k in keys:
            if k not in src or src.get(k) is None:
                missing.append(k)
        return missing

    def _stale_context(self, context: Dict[str, Any], now_ts: int) -> Tuple[bool, str]:
        try:
            as_of = int(context["context_as_of_ts"])
            ttl = int(context["context_ttl_seconds"])
        except Exception:
            return True, "context_missing_or_invalid_time_fields"

        if now_ts < 0 or as_of < 0 or ttl < 0:
            return True, "context_time_fields_negative"

        age = now_ts - as_of
        if age < 0:
            return True, "context_time_in_future_relative_to_now"
        if age > ttl:
            return True, "context_stale"
        return False, ""

    def _mechanical_refusals(self, context: Dict[str, Any], proposal: Dict[str, Any]) -> List[str]:
        reasons: List[str] = []

        missing_ctx = self._missing_keys(context, self._context_keys)
        if missing_ctx:
            reasons.append(f"missing_context_keys:{','.join(sorted(missing_ctx))}")
            return reasons  # fail-closed immediately

        missing_prop = self._missing_keys(proposal, self._proposal_required)
        if missing_prop:
            reasons.append(f"missing_proposal_keys:{','.join(sorted(missing_prop))}")
            return reasons  # fail-closed immediately

        now_ts = int(proposal["now_ts"])
        stale, stale_reason = self._stale_context(context, now_ts)
        if stale:
            reasons.append(stale_reason)
            return reasons

        # Risk gate
        daily_loss = float(context["daily_loss"])
        max_daily_loss = float(context["max_daily_loss"])
        if daily_loss >= max_daily_loss:
            reasons.append("risk_daily_loss_limit_reached_or_exceeded")
            return reasons

        # Trade count gate
        trades_taken = int(context["trades_taken_today"])
        cap = int(context["trade_count_cap"])
        if trades_taken >= cap:
            reasons.append("trade_count_cap_reached_or_exceeded")
            return reasons

        # Instrument must match context
        if str(proposal["instrument"]) != str(context["instrument"]):
            reasons.append("instrument_mismatch_with_context")
            return reasons

        # Proposal must declare max_loss and invalidation in meaningful form (non-empty)
        if str(proposal.get("invalidation", "")).strip() == "":
            reasons.append("proposal_invalidation_missing_or_empty")
            return reasons
        if float(proposal.get("max_loss", 0.0)) <= 0.0:
            reasons.append("proposal_max_loss_missing_or_non_positive")
            return reasons
        if float(proposal.get("size", 0.0)) <= 0.0:
            reasons.append("proposal_size_missing_or_non_positive")
            return reasons
        if str(proposal.get("entry_intent", "")).strip() == "":
            reasons.append("proposal_entry_intent_missing_or_empty")
            return reasons
        if str(proposal.get("time_constraint", "")).strip() == "":
            reasons.append("proposal_time_constraint_missing_or_empty")
            return reasons

        return reasons  # empty => allowed

    def decide_proposal(self, context: Dict[str, Any], proposal: Dict[str, Any]) -> HatOutcome:
        reasons = self._mechanical_refusals(context, proposal)
        decision = HatDecision.REFUSE if reasons else HatDecision.ALLOW
        return HatOutcome(
            hat_name=self.name,
            decision=decision,
            reasons=reasons,
            consumed_context_keys=self.context_keys_consumed(),
            proposal_fingerprint=stable_fingerprint(proposal),
            stage="PROPOSE",
        )

    def decide_commit(
        self,
        context: Dict[str, Any],
        proposed_proposal: Dict[str, Any],
        commit_proposal: Dict[str, Any],
    ) -> HatOutcome:
        # Fail-closed if proposed is missing critical keys
        missing_proposed = self._missing_keys(proposed_proposal, self._proposal_required)
        if missing_proposed:
            reasons = [f"missing_original_proposal_keys:{','.join(sorted(missing_proposed))}"]
            return HatOutcome(
                hat_name=self.name,
                decision=HatDecision.REFUSE,
                reasons=reasons,
                consumed_context_keys=self.context_keys_consumed(),
                proposal_fingerprint=stable_fingerprint(commit_proposal),
                stage="COMMIT",
            )

        # Re-run mechanical checks on commit proposal with current context (still deterministic)
        reasons = self._mechanical_refusals(context, commit_proposal)
        if reasons:
            return HatOutcome(
                hat_name=self.name,
                decision=HatDecision.REFUSE,
                reasons=reasons,
                consumed_context_keys=self.context_keys_consumed(),
                proposal_fingerprint=stable_fingerprint(commit_proposal),
                stage="COMMIT",
            )

        # Re-commit gate: refuse silent drift between propose and commit on key fields
        # (Require operator to explicitly recommit if these change.)
        drift_fields = ["size", "entry_intent", "max_loss", "invalidation", "instrument"]
        drifted: List[str] = []
        for f in drift_fields:
            if str(proposed_proposal.get(f)) != str(commit_proposal.get(f)):
                drifted.append(f)

        if drifted:
            reasons = [f"proposal_drift_requires_recommit:{','.join(sorted(drifted))}"]
            return HatOutcome(
                hat_name=self.name,
                decision=HatDecision.REQUIRE_RECOMMIT,
                reasons=reasons,
                consumed_context_keys=self.context_keys_consumed(),
                proposal_fingerprint=stable_fingerprint(commit_proposal),
                stage="COMMIT",
            )

        return HatOutcome(
            hat_name=self.name,
            decision=HatDecision.ALLOW,
            reasons=[],
            consumed_context_keys=self.context_keys_consumed(),
            proposal_fingerprint=stable_fingerprint(commit_proposal),
            stage="COMMIT",
        )
