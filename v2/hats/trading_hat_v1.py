"""
TRADING HAT v1 (FROZEN)
Governance-only classifier.
- No execution
- No market data
- No advice
Deterministic: same input -> same receipt.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from hashlib import sha256
from typing import Any, Dict, Literal
from v2.hats.hat_interface import HatDecision
HatId = Literal["TRADING_HAT_V1"]
DecisionType = Literal["ALLOW", "REFUSE", "NO-OP"]


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


ALLOWED_INSTRUMENT_TYPES = {"equity", "option", "future", "other"}
ALLOWED_STRATEGY_CLASS = {"defined_strategy", "undefined_strategy"}
ALLOWED_RISK_CLASS = {"low", "medium", "high"}
ALLOWED_TIME_HORIZON = {"intraday", "swing", "long_term"}
ALLOWED_CONTEXT = {"standard", "experimental"}

REASON_CODES = {
    "RECOMMIT_REQUIRED",
    "COMMIT_DRIFT",
    "INSTRUMENT_MISMATCH",
    "STALE_CONTEXT",
    "TRADE_COUNT_CAP_REACHED",
    "RISK_LIMIT_REACHED",
    "MISSING_CONTEXT",
    "NO_EXECUTION",
    "EXCESSIVE_RISK_CLASS",
    "UNCLASSIFIED_STRATEGY",
    "CONTEXT_NOT_GOVERNABLE",
    "OUT_OF_SCOPE_INSTRUMENT",
    "BASELINE_PERMITTED_CASE",
    "MALFORMED_INPUT",
}

RULES_IN_ORDER = [
    "TRD-R-999",
    "TRD-R-001",
    "TRD-R-002",
    "TRD-R-003",
    "TRD-R-004",
    "TRD-R-005",
    "TRD-R-000",
]


@dataclass(frozen=True)
class TradingInput:
    instrument_type: str
    strategy_class: str
    risk_class: str
    time_horizon: str
    leverage_flag: bool
    operator_declared_context: str


def _stable_json(obj: Dict[str, Any]) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _sha256_hex(s: str) -> str:
    return sha256(s.encode("utf-8")).hexdigest()


def validate_input(payload: Dict[str, Any]) -> TradingInput:
    required = [
        "instrument_type",
        "strategy_class",
        "risk_class",
        "time_horizon",
        "leverage_flag",
        "operator_declared_context",
    ]
    for k in required:
        if k not in payload:
            raise ValueError("missing_field:" + k)

    it = payload["instrument_type"]
    sc = payload["strategy_class"]
    rc = payload["risk_class"]
    th = payload["time_horizon"]
    lf = payload["leverage_flag"]
    oc = payload["operator_declared_context"]

    if not isinstance(it, str) or it not in ALLOWED_INSTRUMENT_TYPES:
        raise ValueError("invalid_instrument_type")
    if not isinstance(sc, str) or sc not in ALLOWED_STRATEGY_CLASS:
        raise ValueError("invalid_strategy_class")
    if not isinstance(rc, str) or rc not in ALLOWED_RISK_CLASS:
        raise ValueError("invalid_risk_class")
    if not isinstance(th, str) or th not in ALLOWED_TIME_HORIZON:
        raise ValueError("invalid_time_horizon")
    if not isinstance(lf, bool):
        raise ValueError("invalid_leverage_flag")
    if not isinstance(oc, str) or oc not in ALLOWED_CONTEXT:
        raise ValueError("invalid_operator_declared_context")

    return TradingInput(
        instrument_type=it,
        strategy_class=sc,
        risk_class=rc,
        time_horizon=th,
        leverage_flag=lf,
        operator_declared_context=oc,
    )


def evaluate(payload: Dict[str, Any], logical_time_index: int) -> Dict[str, Any]:
    """
    Deterministic evaluation.
    Returns a receipt dict with a locked schema.
    """
    hat_id: HatId = "TRADING_HAT_V1"
    if not isinstance(logical_time_index, int) or logical_time_index < 0:
        logical_time_index = 0

    try:
        ti = validate_input(payload)
        valid = True
    except Exception:
        ti = None
        valid = False

    normalized = payload if isinstance(payload, dict) else {"_malformed": True}
    input_fingerprint = _sha256_hex(_stable_json(normalized))

    decision_type: DecisionType
    reason_code: str
    rule_id: str

    if not valid:
        decision_type = "REFUSE"
        reason_code = "MALFORMED_INPUT"
        rule_id = "TRD-R-000"
    else:
        assert ti is not None

        if ti.instrument_type == "option" and ti.time_horizon == "intraday" and ti.leverage_flag is True:
            decision_type = "REFUSE"
            reason_code = "EXCESSIVE_RISK_CLASS"
            rule_id = "TRD-R-001"
        elif ti.strategy_class == "undefined_strategy":
            decision_type = "REFUSE"
            reason_code = "UNCLASSIFIED_STRATEGY"
            rule_id = "TRD-R-002"
        elif ti.operator_declared_context == "experimental":
            decision_type = "NO-OP"
            reason_code = "CONTEXT_NOT_GOVERNABLE"
            rule_id = "TRD-R-003"
        elif ti.instrument_type == "other":
            decision_type = "REFUSE"
            reason_code = "OUT_OF_SCOPE_INSTRUMENT"
            rule_id = "TRD-R-004"
        elif (
            ti.instrument_type == "equity"
            and ti.time_horizon == "long_term"
            and ti.leverage_flag is False
            and ti.strategy_class == "defined_strategy"
            and ti.operator_declared_context == "standard"
        ):
            decision_type = "ALLOW"
            reason_code = "BASELINE_PERMITTED_CASE"
            rule_id = "TRD-R-005"
        else:
            decision_type = "REFUSE"
            reason_code = "EXCESSIVE_RISK_CLASS"
            rule_id = "TRD-R-001"

    decision_obj = {
        "hat_id": hat_id,
        "rule_id": rule_id,
        "decision_type": decision_type,
        "reason_code": reason_code,
        "input_fingerprint": input_fingerprint,
        "logical_time_index": int(logical_time_index),
    }
    decision_fingerprint = _sha256_hex(_stable_json(decision_obj))

    receipt = {
        "hat_id": hat_id,
        "rule_id": rule_id,
        "decision_type": decision_type,
        "reason_code": reason_code,
        "input_fingerprint": input_fingerprint,
        "decision_fingerprint": decision_fingerprint,
        "logical_time_index": int(logical_time_index),
    }
    return receipt


def schema_contract() -> Dict[str, Any]:
    """
    Locked receipt schema description (for docs/tests).
    """
    return {
        "hat_id": "TRADING_HAT_V1",
        "decision_type_enum": ["ALLOW", "REFUSE", "NO-OP"],
        "reason_code_enum": sorted(REASON_CODES),
        "rules_in_order": RULES_IN_ORDER,
        "receipt_fields": [
            "hat_id",
            "rule_id",
            "decision_type",
            "reason_code",
            "input_fingerprint",
            "decision_fingerprint",
            "logical_time_index",
        ],
    }


# --------------------------------------------------------------------

# Back-compat surface: TradingHatV1 is required by existing registry/router/tests.
# This class is GOVERNANCE-ONLY and has ZERO execution authority.
# It implements the expected interfaces:
#   - decide_proposal(ctx, proposal)
#   - decide_commit(ctx, proposed, commit)
# Deterministic, fail-closed, no wall-clock dependence (uses provided timestamps only).


# --------------------------------------------------------------------
# TradingHatV1 — expected surface for registry/router/tests
# Returns HatOutcome objects (NOT dicts).
# Governance-only. No execution. Deterministic.
# --------------------------------------------------------------------

class TradingHatV1:
    HAT: str = "TRADING_HAT_V1"

    def hat_id(self) -> str:
        return self.HAT

    def _fp(self, obj: Dict[str, Any]) -> str:
        try:
            return _sha256_hex(_stable_json(obj))
        except Exception:
            return _sha256_hex(_stable_json({"_malformed": True}))

    def _required_ctx_keys(self) -> list[str]:
        return [
            "instrument",
            "max_daily_loss",
            "daily_loss",
            "trades_taken_today",
            "trade_count_cap",
            "context_as_of_ts",
            "context_ttl_seconds",
        ]

    def _required_prop_keys(self) -> list[str]:
        return [
            "instrument",
            "entry_intent",
            "size",
            "max_loss",
            "invalidation",
            "time_constraint",
            "now_ts",
        ]

    def decide_proposal(self, ctx: Dict[str, Any], proposal: Dict[str, Any]) -> HatOutcome:
        consumed: list[str] = []
        prop_fp = self._fp(proposal if isinstance(proposal, dict) else {"_malformed": True})

        if not isinstance(ctx, dict) or not isinstance(proposal, dict):
            return HatOutcome(
                hat=self.HAT,
                stage="PROPOSE",
                decision=HatDecision.REFUSE,
                reasons=["malformed_input"],
                consumed_context_keys=[],
                proposal_fingerprint=prop_fp,
            )

        # required ctx
        for k in self._required_ctx_keys():
            consumed.append(k)
            if k not in ctx:
                return HatOutcome(
                    hat=self.HAT,
                    stage="PROPOSE",
                    decision=HatDecision.REFUSE,
                    reasons=["missing_context_keys:" + k],
                    consumed_context_keys=consumed,
                    proposal_fingerprint=prop_fp,
                )

        # required proposal
        for k in self._required_prop_keys():
            if k not in proposal:
                return HatOutcome(
                    hat=self.HAT,
                    stage="PROPOSE",
                    decision=HatDecision.REFUSE,
                    reasons=["malformed_proposal:" + k],
                    consumed_context_keys=consumed,
                    proposal_fingerprint=prop_fp,
                )

        # instrument match
        if str(proposal.get("instrument")) != str(ctx.get("instrument")):
            return HatOutcome(
                hat=self.HAT,
                stage="PROPOSE",
                decision=HatDecision.REFUSE,
                reasons=["instrument_mismatch_with_context"],
                consumed_context_keys=consumed,
                proposal_fingerprint=prop_fp,
            )

        # staleness check (purely based on provided timestamps)
        try:
            age = float(proposal["now_ts"]) - float(ctx["context_as_of_ts"])
            ttl = float(ctx["context_ttl_seconds"])
            if age > ttl:
                return HatOutcome(
                    hat=self.HAT,
                    stage="PROPOSE",
                    decision=HatDecision.REFUSE,
                    reasons=["context_stale"],
                    consumed_context_keys=consumed,
                    proposal_fingerprint=prop_fp,
                )
        except Exception:
            return HatOutcome(
                hat=self.HAT,
                stage="PROPOSE",
                decision=HatDecision.REFUSE,
                reasons=["malformed_timestamps"],
                consumed_context_keys=consumed,
                proposal_fingerprint=prop_fp,
            )

        # risk limit
        try:
            if float(ctx["daily_loss"]) >= float(ctx["max_daily_loss"]):
                return HatOutcome(
                    hat=self.HAT,
                    stage="PROPOSE",
                    decision=HatDecision.REFUSE,
                    reasons=["risk_daily_loss_limit_reached_or_exceeded"],
                    consumed_context_keys=consumed,
                    proposal_fingerprint=prop_fp,
                )
        except Exception:
            return HatOutcome(
                hat=self.HAT,
                stage="PROPOSE",
                decision=HatDecision.REFUSE,
                reasons=["malformed_risk_fields"],
                consumed_context_keys=consumed,
                proposal_fingerprint=prop_fp,
            )

        # trade count cap
        try:
            if int(ctx["trades_taken_today"]) >= int(ctx["trade_count_cap"]):
                return HatOutcome(
                    hat=self.HAT,
                    stage="PROPOSE",
                    decision=HatDecision.REFUSE,
                    reasons=["trade_count_cap_reached_or_exceeded"],
                    consumed_context_keys=consumed,
                    proposal_fingerprint=prop_fp,
                )
        except Exception:
            return HatOutcome(
                hat=self.HAT,
                stage="PROPOSE",
                decision=HatDecision.REFUSE,
                reasons=["malformed_trade_count_fields"],
                consumed_context_keys=consumed,
                proposal_fingerprint=prop_fp,
            )

        return HatOutcome(
            hat=self.HAT,
            stage="PROPOSE",
            decision=HatDecision.ALLOW,
            reasons=["ok"],
            consumed_context_keys=consumed,
            proposal_fingerprint=prop_fp,
        )

    def decide_commit(self, ctx: Dict[str, Any], proposed: Dict[str, Any], commit: Dict[str, Any]) -> HatOutcome:
        prop_fp = self._fp(proposed if isinstance(proposed, dict) else {"_malformed": True})
        commit_fp = self._fp(commit if isinstance(commit, dict) else {"_malformed": True})

        if not isinstance(ctx, dict) or not isinstance(proposed, dict) or not isinstance(commit, dict):
            return HatOutcome(
                hat=self.HAT,
                stage="COMMIT",
                decision=HatDecision.REFUSE,
                reasons=["malformed_input"],
                consumed_context_keys=[],
                proposal_fingerprint=prop_fp,
                commit_fingerprint=commit_fp,
            )

        # proposal must be allowed
        prop_out = self.decide_proposal(ctx, proposed)
        if prop_out.decision != HatDecision.ALLOW:
            return HatOutcome(
                hat=self.HAT,
                stage="COMMIT",
                decision=HatDecision.REFUSE,
                reasons=["proposal_not_allowed"] + list(prop_out.reasons),
                consumed_context_keys=list(prop_out.consumed_context_keys),
                proposal_fingerprint=prop_out.proposal_fingerprint,
                commit_fingerprint=commit_fp,
            )

        # require recommit on ANY drift
        drift = []
        for k in sorted(set(proposed.keys()) | set(commit.keys())):
            if proposed.get(k) != commit.get(k):
                drift.append(k)

        if drift:
            return HatOutcome(
                hat=self.HAT,
                stage="COMMIT",
                decision=HatDecision.REQUIRE_RECOMMIT,
                reasons=["proposal_drift_requires_recommit:" + ",".join(drift)],
                consumed_context_keys=list(prop_out.consumed_context_keys),
                proposal_fingerprint=prop_out.proposal_fingerprint,
                commit_fingerprint=commit_fp,
            )

        return HatOutcome(
            hat=self.HAT,
            stage="COMMIT",
            decision=HatDecision.ALLOW,
            reasons=[],
            consumed_context_keys=list(prop_out.consumed_context_keys),
            proposal_fingerprint=prop_out.proposal_fingerprint,
            commit_fingerprint=commit_fp,
        )
