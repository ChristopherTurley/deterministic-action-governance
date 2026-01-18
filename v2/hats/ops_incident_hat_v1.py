"""
OPS INCIDENT HAT v1 (governance-only, deterministic)

Goal:
- Enforce fail-closed operational governance during incidents.
- This hat does NOT execute actions, automate, integrate, or advise.
- It produces deterministic decisions + auditable receipts.

Scope (minimal, load-bearing):
- Stale context refusal
- Incident mode restrictions on risky ops
- Explicit recommit requirement on commit drift
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
    stage: str
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


class OpsIncidentHatV1:
    HAT: str = "OPS_INCIDENT_HAT_V1"
    PREFIX: str = "INV_OPS_"

    def hat_id(self) -> str:
        return self.HAT

    def _r(self, token: str) -> str:
        return self.PREFIX + token

    def _fp(self, obj: Dict[str, Any]) -> str:
        try:
            return _sha256_hex(_stable_json(obj))
        except Exception:
            return _sha256_hex(_stable_json({"_malformed": True}))

    def _required_ctx(self) -> list[str]:
        return [
            "incident_mode",          # bool
            "severity",               # "SEV0"|"SEV1"|"SEV2"|"SEV3"
            "change_freeze",          # bool (incident freeze)
            "context_as_of_ts",
            "context_ttl_seconds",
        ]

    def _required_prop(self) -> list[str]:
        return [
            "op_type",                # "deploy"|"config_change"|"restart"|"access_change"
            "risk_level",             # "LOW"|"MEDIUM"|"HIGH"
            "now_ts",
            "summary",
        ]

    def decide_proposal(self, ctx: Dict[str, Any], proposal: Dict[str, Any]) -> HatOutcome:
        consumed: list[str] = []
        prop_fp = self._fp(proposal if isinstance(proposal, dict) else {"_malformed": True})

        if not isinstance(ctx, dict) or not isinstance(proposal, dict):
            return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, [self._r("malformed_input")], [], prop_fp)

        for k in self._required_ctx():
            consumed.append(k)
            if k not in ctx:
                return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, [self._r("missing_context_keys:" + k)], consumed, prop_fp)

        for k in self._required_prop():
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

        # incident gating (minimal deterministic policy)
        try:
            incident = bool(ctx["incident_mode"])
            freeze = bool(ctx["change_freeze"])
            op = str(proposal["op_type"])
            risk = str(proposal["risk_level"])

            if incident and freeze:
                # During incident freeze, block HIGH risk ops always, and block deploy/config/access by default.
                if risk == "HIGH":
                    return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, [self._r("incident_freeze_blocks_high_risk_ops")], consumed, prop_fp)
                if op in {"deploy", "config_change", "access_change"}:
                    return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, [self._r("incident_freeze_blocks_risky_op_type:" + op)], consumed, prop_fp)
        except Exception:
            return HatOutcome(self.HAT, "PROPOSE", HatDecision.REFUSE, [self._r("malformed_incident_fields")], consumed, prop_fp)

        return HatOutcome(self.HAT, "PROPOSE", HatDecision.ALLOW, [], consumed, prop_fp)

    def decide_commit(self, ctx: Dict[str, Any], proposed: Dict[str, Any], commit: Dict[str, Any]) -> HatOutcome:
        prop_fp = self._fp(proposed if isinstance(proposed, dict) else {"_malformed": True})
        commit_fp = self._fp(commit if isinstance(commit, dict) else {"_malformed": True})

        if not isinstance(ctx, dict) or not isinstance(proposed, dict) or not isinstance(commit, dict):
            return HatOutcome(self.HAT, "COMMIT", HatDecision.REFUSE, [self._r("malformed_input")], [], prop_fp, commit_fp)

        p = self.decide_proposal(ctx, proposed)
        if p.decision != HatDecision.ALLOW:
            return HatOutcome(self.HAT, "COMMIT", HatDecision.REFUSE, [self._r("proposal_not_allowed")] + list(p.reasons), list(p.consumed_context_keys), p.proposal_fingerprint, commit_fp)

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
                list(p.consumed_context_keys),
                p.proposal_fingerprint,
                commit_fp,
            )

        return HatOutcome(self.HAT, "COMMIT", HatDecision.ALLOW, [], list(p.consumed_context_keys), p.proposal_fingerprint, commit_fp)
