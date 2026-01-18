"""
EDUCATION HAT v1 (governance-only, deterministic)
Purpose: enforce education governance boundaries:
- refuses requests that enable academic cheating or plagiarism
- refuses "do my assignment/test" style requests
- allows tutoring-style support only (explanations, study plans, practice problems)
- strict stale-context refusal
No execution. No automation. No integration. No hidden assistance.
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


class EducationHatV1:
    HAT: str = "EDUCATION_HAT_V1"
    PREFIX: str = "INV_EDU_"

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
            "role",  # "student"|"teacher"|"admin" (classification only)
            "assessment_mode",  # bool (true => stricter)
            "context_as_of_ts",
            "context_ttl_seconds",
        ]

    def _required_prop_keys(self) -> list[str]:
        return [
            "request_type",  # "tutoring"|"answer_key"|"rewrite"|"test_help"
            "topic",
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

        try:
            req_type = str(proposal.get("request_type", "")).lower().strip()
            topic = str(proposal.get("topic", "")).lower().strip()
            assessment = bool(ctx.get("assessment_mode"))

            cheating_signals = [
                "answer", "answer key", "solutions", "solve for me", "do my homework", "write my essay",
                "take-home exam", "quiz", "test", "midterm", "final", "plagiarize", "copy", "cheat"
            ]

            # Explicit cheat / answer-key style requests => refuse
            if req_type in ('answer_key', 'test_help'):
                return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, [self._r("academic_integrity_violation_cheating_request")], consumed, prop_fp)

            # Assessment mode: stricter, refuse ambiguous "just give me the answer" signals
            if assessment and any(s in topic for s in ["answer", "solutions", "solve"]):
                return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, [self._r("assessment_mode_blocks_direct_answers")], consumed, prop_fp)

            # Rewrite requests that imply plagiarism
            if req_type == "rewrite" and any(s in topic for s in ["plagiar", "copy", "steal", "turnitin"]):
                return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, [self._r("academic_integrity_violation_plagiarism_facilitation")], consumed, prop_fp)

            # Generic cheating signals in summary/topic => refuse
            if any(s in topic for s in cheating_signals):
                return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, [self._r("academic_integrity_violation_cheating_request")], consumed, prop_fp)

            # Tutoring allowed
            if req_type == "tutoring":
                return HatOutcome(self.HAT, "PROPOSE", HatDecision.ALLOW, [], consumed, prop_fp)

            # Default: fail-closed for unknown request types
            return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, [self._r("unknown_request_type_fail_closed")], consumed, prop_fp)

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
