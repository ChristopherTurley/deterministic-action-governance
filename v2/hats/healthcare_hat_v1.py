"""
HEALTHCARE HAT v1 (governance-only, deterministic)
Purpose: enforce healthcare safety/governance boundaries without execution:
- refuses medical diagnosis / prescribing / emergency instructions
- allows only admin/operational requests (scheduling, billing, record request)
- strict stale-context refusal
No execution. No automation. No integration. No advice beyond refusal semantics.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from hashlib import sha256
from typing import Any, Dict

from v2.hats.hat_interface import HatDecision


def _stable_json(obj: Dict[str, Any]) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _sha256_hex(s: str) -> str:
    return sha256(s.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class HatOutcome:
    hat: str
    stage: str  # "PROPOSE" | "COMMIT"
    decision: HatDecision
    reasons: list[str]
    consumed_context_keys: list[str]
    proposal_fingerprint: str
    commit_fingerprint: str | None = None

    def to_ledger_event(self) -> dict:
        e = {
            "type": "HAT_DECISION",
            "hat": self.hat,
            "stage": self.stage,
            "decision": self.decision.value,
            "reasons": list(self.reasons),
            "consumed_context_keys": list(self.consumed_context_keys),
            "proposal_fingerprint": self.proposal_fingerprint,
        }
        if self.commit_fingerprint is not None:
            e["commit_fingerprint"] = self.commit_fingerprint
        return e


class HealthcareHatV1:
    HAT: str = "HEALTHCARE_HAT_V1"
    PREFIX: str = "INV_HEALTH_"

    def hat_id(self) -> str:
        return self.HAT

    def _r(self, token: str) -> str:
        return self.PREFIX + token

    def _fp(self, obj: Dict[str, Any]) -> str:
        try:
            if not isinstance(obj, dict):
                return _sha256_hex(_stable_json({"_malformed": True}))
            return _sha256_hex(_stable_json(obj))
        except Exception:
            return _sha256_hex(_stable_json({"_malformed": True}))

    def _required_ctx_keys(self) -> list[str]:
        return [
            "org_mode",  # "admin"|"clinical" (governance classification only)
            "restricted_mode",  # bool
            "context_as_of_ts",
            "context_ttl_seconds",
        ]

    def _required_prop_keys(self) -> list[str]:
        return [
            "request_type",  # "admin"|"clinical"
            "topic",         # string
            "now_ts",
            "summary",
        ]

    def decide_proposal(self, ctx: Dict[str, Any], proposal: Dict[str, Any]) -> HatOutcome:
        consumed: list[str] = []
        prop_fp = self._fp(proposal)

        if not isinstance(ctx, dict) or not isinstance(proposal, dict):
            return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, [self._r("malformed_input")], [], prop_fp)

        for k in self._required_ctx_keys():
            consumed.append(k)
            if k not in ctx:
                return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, [self._r("missing_context_keys:" + k)], consumed, prop_fp)

        for k in self._required_prop_keys():
            if k not in proposal:
                return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, [self._r("malformed_proposal:" + k)], consumed, prop_fp)

        # staleness
        try:
            age = float(proposal["now_ts"]) - float(ctx["context_as_of_ts"])
            ttl = float(ctx["context_ttl_seconds"])
            if age > ttl:
                return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, [self._r("context_stale")], consumed, prop_fp)
        except Exception:
            return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, [self._r("malformed_timestamps")], consumed, prop_fp)

        # hard governance boundaries (no clinical guidance)
        try:
            req_type = str(proposal.get("request_type", "")).lower().strip()
            topic = str(proposal.get("topic", "")).lower().strip()
            restricted = bool(ctx.get("restricted_mode"))

            # Anything clinical => refuse (diagnosis/prescription/emergency instructions)
            if req_type == "clinical":
                return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, [self._r("clinical_advice_or_diagnosis_disallowed")], consumed, prop_fp)

            # Restricted mode blocks sharing PHI-like info in freeform
            if restricted and any(x in topic for x in ["medical record", "phi", "lab result", "diagnosis", "prescription"]):
                return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, [self._r("restricted_mode_blocks_sensitive_health_data")], consumed, prop_fp)

            # Otherwise allow only admin-like topics
            # (appointments, billing, insurance, records request routing without content)
            return HatOutcome(self.HAT, "PROPOSE", HatDecision.ALLOW, [], consumed, prop_fp)

        except Exception:
            return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, [self._r("malformed_request_fields")], consumed, prop_fp)

    def decide_commit(self, ctx: Dict[str, Any], proposed: Dict[str, Any], commit: Dict[str, Any]) -> HatOutcome:
        prop_fp = self._fp(proposed)
        commit_fp = self._fp(commit)

        if not isinstance(ctx, dict) or not isinstance(proposed, dict) or not isinstance(commit, dict):
            return HatOutcome(self.HAT, "COMMIT", HatDecision.REFUSE, [self._r("malformed_input")], [], prop_fp, commit_fp)

        prop_out = self.decide_proposal(ctx, proposed)
        if prop_out.decision != HatDecision.ALLOW:
            return HatOutcome(self.HAT, "COMMIT", HatDecision.REFUSE, [self._r("proposal_not_allowed")] + list(prop_out.reasons), list(prop_out.consumed_context_keys), prop_out.proposal_fingerprint, commit_fp)

        drift = []
        for k in sorted(set(proposed.keys()) | set(commit.keys())):
            if proposed.get(k) != commit.get(k):
                drift.append(k)

        if drift:
            return HatOutcome(
                self.HAT,
                "COMMIT",
                HatDecision.REQUIRE_RECOMMIT,
                [self._r("proposal_drift_requires_recommit:" + ",".join(drift))],
                list(prop_out.consumed_context_keys),
                prop_out.proposal_fingerprint,
                commit_fp,
            )

        return HatOutcome(self.HAT, "COMMIT", HatDecision.ALLOW, [], list(prop_out.consumed_context_keys), prop_out.proposal_fingerprint, commit_fp)
