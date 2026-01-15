from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from v2.hats.hat_interface import HatDecision


@dataclass(frozen=True)
class HatOutcome:
    decision: HatDecision
    reasons: List[str]
    consumed_context_keys: List[str]
    proposal_fingerprint: str
    hat: str
    stage: str

    def to_ledger_event(self) -> Dict[str, Any]:
        return {
            "type": "HAT_DECISION",
            "hat": self.hat,
            "stage": self.stage,
            "decision": self.decision.value,
            "reasons": list(self.reasons),
            "consumed_context_keys": list(self.consumed_context_keys),
            "proposal_fingerprint": self.proposal_fingerprint,
        }


def _stable_fingerprint(payload: Dict[str, Any]) -> str:
    # Import locally to avoid global side effects.
    import hashlib
    import json

    blob = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


class FocusHatV1:
    """
    Focus Hat v1: deterministic enforcement of attention/session constraints.
    - No strategy generation
    - No autonomy
    - Fail-closed validation
    """

    NAME = "FOCUS_HAT_V1"

    CONSUMED_CONTEXT_KEYS = [
        "focus_mode",
        "context_as_of_ts",
        "context_ttl_seconds",
        "task_count_cap",
        "tasks_remaining",
        "minutes_cap",
        "minutes_remaining",
    ]

    PROPOSAL_REQUIRED_KEYS = [
        "task_count",
    ]

    # Optional proposal key
    PROPOSAL_OPTIONAL_KEYS = [
        "planned_minutes",
    ]

    def name(self) -> str:
        return self.NAME

    def consumed_context_keys(self) -> List[str]:
        return list(self.CONSUMED_CONTEXT_KEYS)

    def proposal_schema_requirements(self) -> List[str]:
        return list(self.PROPOSAL_REQUIRED_KEYS)

    def _validate_context(self, ctx: Dict[str, Any], now_ts: int) -> List[str]:
        reasons: List[str] = []

        required = [
            "focus_mode",
            "context_as_of_ts",
            "context_ttl_seconds",
            "task_count_cap",
            "tasks_remaining",
        ]
        for k in required:
            if k not in ctx or ctx.get(k) is None:
                reasons.append("context_missing_required_key:" + k)

        if reasons:
            return reasons

        as_of = int(ctx["context_as_of_ts"])
        ttl = int(ctx["context_ttl_seconds"])
        age = now_ts - as_of
        if age > ttl:
            reasons.append("context_stale_ttl_exceeded")

        return reasons

    def _validate_proposal(self, proposal: Dict[str, Any]) -> List[str]:
        reasons: List[str] = []

        for k in self.PROPOSAL_REQUIRED_KEYS:
            if k not in proposal or proposal.get(k) is None:
                reasons.append("proposal_missing_required_key:" + k)

        # Planned minutes is optional, but if present must be numeric-ish
        if "planned_minutes" in proposal and proposal.get("planned_minutes") is not None:
            try:
                float(proposal["planned_minutes"])
            except Exception:
                reasons.append("proposal_invalid_number:planned_minutes")

        # task_count must be numeric-ish
        if "task_count" in proposal and proposal.get("task_count") is not None:
            try:
                float(proposal["task_count"])
            except Exception:
                reasons.append("proposal_invalid_number:task_count")

        return reasons

    def decide_proposal(self, ctx: Dict[str, Any], proposal: Dict[str, Any]) -> HatOutcome:
        now_ts = int(proposal.get("now_ts", ctx.get("context_as_of_ts", 0)))

        ctx_reasons = self._validate_context(ctx, now_ts)
        if ctx_reasons:
            fp = _stable_fingerprint({"stage": "PROPOSE", "ctx": ctx, "proposal": proposal})
            return HatOutcome(
                decision=HatDecision.REFUSE,
                reasons=ctx_reasons,
                consumed_context_keys=self.consumed_context_keys(),
                proposal_fingerprint=fp,
                hat=self.NAME,
                stage="PROPOSE",
            )

        prop_reasons = self._validate_proposal(proposal)
        if prop_reasons:
            fp = _stable_fingerprint({"stage": "PROPOSE", "ctx": ctx, "proposal": proposal})
            return HatOutcome(
                decision=HatDecision.REFUSE,
                reasons=prop_reasons,
                consumed_context_keys=self.consumed_context_keys(),
                proposal_fingerprint=fp,
                hat=self.NAME,
                stage="PROPOSE",
            )

        # Enforce caps
        task_count = float(proposal["task_count"])
        task_cap = float(ctx["task_count_cap"])
        tasks_remaining = float(ctx["tasks_remaining"])

        if tasks_remaining <= 0:
            fp = _stable_fingerprint({"stage": "PROPOSE", "ctx": ctx, "proposal": proposal})
            return HatOutcome(
                decision=HatDecision.REFUSE,
                reasons=["focus_no_tasks_remaining"],
                consumed_context_keys=self.consumed_context_keys(),
                proposal_fingerprint=fp,
                hat=self.NAME,
                stage="PROPOSE",
            )

        if task_count > task_cap:
            fp = _stable_fingerprint({"stage": "PROPOSE", "ctx": ctx, "proposal": proposal})
            return HatOutcome(
                decision=HatDecision.REFUSE,
                reasons=["focus_task_count_exceeds_cap"],
                consumed_context_keys=self.consumed_context_keys(),
                proposal_fingerprint=fp,
                hat=self.NAME,
                stage="PROPOSE",
            )

        if task_count > tasks_remaining:
            fp = _stable_fingerprint({"stage": "PROPOSE", "ctx": ctx, "proposal": proposal})
            return HatOutcome(
                decision=HatDecision.REFUSE,
                reasons=["focus_task_count_exceeds_remaining"],
                consumed_context_keys=self.consumed_context_keys(),
                proposal_fingerprint=fp,
                hat=self.NAME,
                stage="PROPOSE",
            )

        if "planned_minutes" in proposal and proposal.get("planned_minutes") is not None:
            if "minutes_cap" not in ctx or ctx.get("minutes_cap") is None:
                fp = _stable_fingerprint({"stage": "PROPOSE", "ctx": ctx, "proposal": proposal})
                return HatOutcome(
                    decision=HatDecision.REFUSE,
                    reasons=["context_missing_required_key:minutes_cap"],
                    consumed_context_keys=self.consumed_context_keys(),
                    proposal_fingerprint=fp,
                    hat=self.NAME,
                    stage="PROPOSE",
                )
            if "minutes_remaining" not in ctx or ctx.get("minutes_remaining") is None:
                fp = _stable_fingerprint({"stage": "PROPOSE", "ctx": ctx, "proposal": proposal})
                return HatOutcome(
                    decision=HatDecision.REFUSE,
                    reasons=["context_missing_required_key:minutes_remaining"],
                    consumed_context_keys=self.consumed_context_keys(),
                    proposal_fingerprint=fp,
                    hat=self.NAME,
                    stage="PROPOSE",
                )

            planned = float(proposal["planned_minutes"])
            cap = float(ctx["minutes_cap"])
            remaining = float(ctx["minutes_remaining"])

            if planned > cap:
                fp = _stable_fingerprint({"stage": "PROPOSE", "ctx": ctx, "proposal": proposal})
                return HatOutcome(
                    decision=HatDecision.REFUSE,
                    reasons=["focus_planned_minutes_exceeds_cap"],
                    consumed_context_keys=self.consumed_context_keys(),
                    proposal_fingerprint=fp,
                    hat=self.NAME,
                    stage="PROPOSE",
                )

            if planned > remaining:
                fp = _stable_fingerprint({"stage": "PROPOSE", "ctx": ctx, "proposal": proposal})
                return HatOutcome(
                    decision=HatDecision.REFUSE,
                    reasons=["focus_planned_minutes_exceeds_remaining"],
                    consumed_context_keys=self.consumed_context_keys(),
                    proposal_fingerprint=fp,
                    hat=self.NAME,
                    stage="PROPOSE",
                )

        fp_ok = _stable_fingerprint({"stage": "PROPOSE_OK", "ctx": ctx, "proposal": proposal})
        return HatOutcome(
            decision=HatDecision.ALLOW,
            reasons=[],
            consumed_context_keys=self.consumed_context_keys(),
            proposal_fingerprint=fp_ok,
            hat=self.NAME,
            stage="PROPOSE",
        )

    def decide_commit(self, ctx: Dict[str, Any], proposed: Dict[str, Any], commit: Dict[str, Any]) -> HatOutcome:
        now_ts = int(commit.get("now_ts", proposed.get("now_ts", ctx.get("context_as_of_ts", 0))))

        ctx_reasons = self._validate_context(ctx, now_ts)
        if ctx_reasons:
            fp = _stable_fingerprint({"stage": "COMMIT", "ctx": ctx, "proposed": proposed, "commit": commit})
            return HatOutcome(
                decision=HatDecision.REFUSE,
                reasons=ctx_reasons,
                consumed_context_keys=self.consumed_context_keys(),
                proposal_fingerprint=fp,
                hat=self.NAME,
                stage="COMMIT",
            )

        drift: List[str] = []
        protected = ["task_count", "planned_minutes"]

        for k in protected:
            a = proposed.get(k, None)
            b = commit.get(k, None)
            # Only compare planned_minutes if it existed in proposed
            if k == "planned_minutes" and a is None:
                continue
            if a != b:
                drift.append(k)

        if drift:
            fp = _stable_fingerprint({"stage": "COMMIT_DRIFT", "ctx": ctx, "proposed": proposed, "commit": commit})
            return HatOutcome(
                decision=HatDecision.REQUIRE_RECOMMIT,
                reasons=["proposal_drift_requires_recommit:" + ",".join(drift)],
                consumed_context_keys=self.consumed_context_keys(),
                proposal_fingerprint=fp,
                hat=self.NAME,
                stage="COMMIT",
            )

        # Validate commit as a proposal (fail-closed)
        prop_reasons = self._validate_proposal(commit)
        if prop_reasons:
            fp = _stable_fingerprint({"stage": "COMMIT_INVALID", "ctx": ctx, "commit": commit})
            return HatOutcome(
                decision=HatDecision.REFUSE,
                reasons=prop_reasons,
                consumed_context_keys=self.consumed_context_keys(),
                proposal_fingerprint=fp,
                hat=self.NAME,
                stage="COMMIT",
            )

        fp_ok = _stable_fingerprint({"stage": "COMMIT_OK", "ctx": ctx, "proposed": proposed, "commit": commit})
        return HatOutcome(
            decision=HatDecision.ALLOW,
            reasons=[],
            consumed_context_keys=self.consumed_context_keys(),
            proposal_fingerprint=fp_ok,
            hat=self.NAME,
            stage="COMMIT",
        )
