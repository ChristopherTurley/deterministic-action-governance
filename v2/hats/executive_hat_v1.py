"""
EXECUTIVE HAT v1 (FROZEN TARGET)
Governance-only. Deterministic. No execution. No advice.
Purpose: enforce executive-decision governance boundaries:
- approval gates
- spend threshold controls
- data classification & sharing refusal
- external comms restrictions
- time-sensitivity / stale context refusal
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from hashlib import sha256
from typing import Any, Dict

from v2.hats.hat_interface import HatDecision  # source-of-truth enum in this repo


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


class ExecutiveHatV1:
    HAT: str = "EXECUTIVE_HAT_V1"

    # Context keys are explicit to make “consumed_context_keys” auditable.
    def _required_ctx_keys(self) -> list[str]:
        return [
            "role",  # "CEO"|"CFO"|"COO"|...
            "approval_limit_usd",
            "approvals_used_today",
            "approval_count_cap",
            "context_as_of_ts",
            "context_ttl_seconds",
            "policy_mode",  # "standard"|"restricted"
        ]

    def _required_prop_keys(self) -> list[str]:
        return [
            "request_type",  # "spend"|"share"|"comms"|"hire"|"strategy"
            "amount_usd",    # numeric
            "data_classification",  # "public"|"internal"|"confidential"|"restricted"
            "external_recipient",   # bool
            "now_ts",               # numeric
            "summary",              # short text
        ]

    def hat_id(self) -> str:
        return self.HAT

    def _fp(self, obj: Dict[str, Any]) -> str:
        try:
            return _sha256_hex(_stable_json(obj))
        except Exception:
            return _sha256_hex(_stable_json({"_malformed": True}))

    def decide_proposal(self, ctx: Dict[str, Any], proposal: Dict[str, Any]) -> HatOutcome:
        consumed: list[str] = []
        prop_fp = self._fp(proposal if isinstance(proposal, dict) else {"_malformed": True})

        if not isinstance(ctx, dict) or not isinstance(proposal, dict):
            return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, ["INV_EXEC_malformed_input"], [], prop_fp)

        # required ctx
        for k in self._required_ctx_keys():
            consumed.append(k)
            if k not in ctx:
                return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, ["INV_EXEC_missing_context_keys:" + k], consumed, prop_fp)

        # required proposal
        for k in self._required_prop_keys():
            if k not in proposal:
                return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, ["INV_EXEC_malformed_proposal:" + k], consumed, prop_fp)

        # staleness (purely based on provided timestamps)
        try:
            age = float(proposal["now_ts"]) - float(ctx["context_as_of_ts"])
            ttl = float(ctx["context_ttl_seconds"])
            if age > ttl:
                return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, ["INV_EXEC_context_stale"], consumed, prop_fp)
        except Exception:
            return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, ["INV_EXEC_malformed_timestamps"], consumed, prop_fp)

        # policy mode restricted => refuse high-risk actions
        if str(ctx.get("policy_mode")) == "restricted":
            if proposal.get("request_type") in {"share", "comms"} and bool(proposal.get("external_recipient")) is True:
                return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, ["INV_EXEC_restricted_mode_blocks_external_comms_or_sharing"], consumed, prop_fp)

        # data classification: confidential/restricted to external => refuse
        try:
            dc = str(proposal.get("data_classification"))
            ext = bool(proposal.get("external_recipient"))
            if ext and dc in {"confidential", "restricted"}:
                return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, ["INV_EXEC_external_sharing_blocked_for_sensitive_data"], consumed, prop_fp)
        except Exception:
            return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, ["INV_EXEC_malformed_data_fields"], consumed, prop_fp)

        # approvals cap
        try:
            if int(ctx["approvals_used_today"]) >= int(ctx["approval_count_cap"]):
                return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, ["INV_EXEC_approval_count_cap_reached_or_exceeded"], consumed, prop_fp)
        except Exception:
            return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, ["INV_EXEC_malformed_approval_fields"], consumed, prop_fp)

        # spend threshold
        try:
            amt = float(proposal["amount_usd"])
            limit = float(ctx["approval_limit_usd"])
            if proposal.get("request_type") == "spend" and amt > limit:
                return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, ["INV_EXEC_spend_exceeds_approval_limit"], consumed, prop_fp)
        except Exception:
            return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, ["INV_EXEC_malformed_amount_fields"], consumed, prop_fp)

        # allowed
        return HatOutcome(self.HAT, "PROPOSE", HatDecision.ALLOW, [], consumed, prop_fp)

    def decide_commit(self, ctx: Dict[str, Any], proposed: Dict[str, Any], commit: Dict[str, Any]) -> HatOutcome:
        prop_fp = self._fp(proposed if isinstance(proposed, dict) else {"_malformed": True})
        commit_fp = self._fp(commit if isinstance(commit, dict) else {"_malformed": True})

        if not isinstance(ctx, dict) or not isinstance(proposed, dict) or not isinstance(commit, dict):
            return HatOutcome(self.HAT, "COMMIT", HatDecision.REFUSE, ["INV_EXEC_malformed_input"], [], prop_fp, commit_fp)

        prop_out = self.decide_proposal(ctx, proposed)
        if prop_out.decision != HatDecision.ALLOW:
            return HatOutcome(self.HAT, "COMMIT", HatDecision.REFUSE, ["INV_EXEC_proposal_not_allowed"] + list(prop_out.reasons), list(prop_out.consumed_context_keys), prop_out.proposal_fingerprint, commit_fp)

        drift = []
        for k in sorted(set(proposed.keys()) | set(commit.keys())):
            if proposed.get(k) != commit.get(k):
                drift.append(k)

        if drift:
            return HatOutcome(self.HAT, "COMMIT", HatDecision.REQUIRE_RECOMMIT, ["INV_EXEC_proposal_drift_requires_recommit:" + ",".join(drift)], list(prop_out.consumed_context_keys), prop_out.proposal_fingerprint, commit_fp)

        return HatOutcome(self.HAT, "COMMIT", HatDecision.ALLOW, [], list(prop_out.consumed_context_keys), prop_out.proposal_fingerprint, commit_fp)
