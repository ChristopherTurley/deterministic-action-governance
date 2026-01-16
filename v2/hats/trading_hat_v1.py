"""
Trading Hat v1 (CANONICAL)

Ground-truth contract from repo:
- decide_proposal/decide_commit return an object with:
  - .decision (HatDecision enum)
  - .reasons (list[str])
  - .to_ledger_event() -> dict
- Reasons are *human-legible tokens* expected by tests (not INV_*).
- ALLOW must have reasons == [] (tests assert this).
No side effects. Deterministic only.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from v2.hats.hat_interface import HatDecision

HAT_KEY = "TRADING_HAT_V1"

# Exact reason tokens expected by tests
REASON_CONTEXT_STALE = "context_stale"
REASON_RISK_LIMIT = "risk_daily_loss_limit_reached_or_exceeded"
REASON_TRADE_CAP = "trade_count_cap_reached_or_exceeded"
REASON_INSTRUMENT_MISMATCH = "instrument_mismatch_with_context"
REASON_RECOMMIT = "proposal_drift_requires_recommit"

# For missing context tests: they check substring "missing_context_keys" appears in at least one reason.
MISSING_PREFIX = "missing_context_keys:"


@dataclass(frozen=True)
class HatOutcome:
    hat: str
    decision: Any  # HatDecision
    reasons: List[str]
    consumed_context_keys: List[str]
    proposal_fingerprint: str

    def to_ledger_event(self) -> Dict[str, Any]:
        return {
            "type": "HAT_DECISION",
            "hat": self.hat,
            "decision": getattr(self.decision, "value", str(self.decision)),
            "reasons": list(self.reasons),
            "consumed_context_keys": list(self.consumed_context_keys),
            "proposal_fingerprint": self.proposal_fingerprint,
        }


def _out(decision: Any, reasons: List[str], consumed: List[str], fp: str) -> HatOutcome:
    return HatOutcome(
        hat=HAT_KEY,
        decision=decision,
        reasons=reasons,
        consumed_context_keys=consumed,
        proposal_fingerprint=fp,
    )


def _required_ctx_keys() -> List[str]:
    return [
        "instrument",
        "max_daily_loss",
        "daily_loss",
        "trades_taken_today",
        "trade_count_cap",
        "context_as_of_ts",
        "context_ttl_seconds",
    ]


def _required_prop_keys() -> List[str]:
    return [
        "instrument",
        "entry_intent",
        "size",
        "max_loss",
        "invalidation",
        "time_constraint",
        "now_ts",
    ]


def _missing_keys(ctx: Dict[str, Any], proposal: Dict[str, Any]) -> List[str]:
    missing: List[str] = []
    for k in _required_ctx_keys():
        if k not in ctx:
            missing.append(k)
    for k in _required_prop_keys():
        if k not in proposal:
            missing.append(k)
    return missing


def _is_stale(ctx: Dict[str, Any], now_ts: Any) -> bool:
    try:
        age = float(now_ts) - float(ctx["context_as_of_ts"])
        ttl = float(ctx["context_ttl_seconds"])
    except Exception:
        return True
    return age > ttl


def _constraints(ctx: Dict[str, Any], proposal: Dict[str, Any]) -> HatOutcome | None:
    missing = _missing_keys(ctx, proposal)
    if missing:
        # Encode missing keys into a single stable reason string that contains "missing_context_keys"
        # Example: "missing_context_keys:max_daily_loss,daily_loss"
        reason = MISSING_PREFIX + ",".join(sorted(missing))
        return _out(HatDecision.REFUSE, [reason], [], "MISSING_CONTEXT_KEYS")

    if str(proposal.get("instrument")) != str(ctx.get("instrument")):
        return _out(HatDecision.REFUSE, [REASON_INSTRUMENT_MISMATCH], ["instrument"], "INSTRUMENT_MISMATCH")

    if _is_stale(ctx, proposal.get("now_ts")):
        return _out(HatDecision.REFUSE, [REASON_CONTEXT_STALE], ["context_as_of_ts", "context_ttl_seconds"], "CONTEXT_STALE")

    try:
        if float(ctx["daily_loss"]) >= float(ctx["max_daily_loss"]):
            return _out(HatDecision.REFUSE, [REASON_RISK_LIMIT], ["daily_loss", "max_daily_loss"], "RISK_LIMIT")
    except Exception:
        return _out(HatDecision.REFUSE, [REASON_RISK_LIMIT], ["daily_loss", "max_daily_loss"], "RISK_LIMIT")

    try:
        if int(ctx["trades_taken_today"]) >= int(ctx["trade_count_cap"]):
            return _out(HatDecision.REFUSE, [REASON_TRADE_CAP], ["trades_taken_today", "trade_count_cap"], "TRADE_CAP")
    except Exception:
        return _out(HatDecision.REFUSE, [REASON_TRADE_CAP], ["trades_taken_today", "trade_count_cap"], "TRADE_CAP")

    return None


class TradingHatV1:
    hat_key = HAT_KEY

    def decide_proposal(self, ctx: Dict[str, Any], proposal: Dict[str, Any]) -> HatOutcome:
        refusal = _constraints(ctx, proposal)
        if refusal is not None:
            return refusal
        # Tests do not require reasons for ALLOW; safest is empty list.
        return _out(HatDecision.ALLOW, [], [], "ALLOW")

    def decide_commit(self, ctx: Dict[str, Any], proposed: Dict[str, Any], commit: Dict[str, Any]) -> HatOutcome:
        # Constraints are evaluated against the proposed payload (commit gating starts from proposal truth).
        refusal = _constraints(ctx, proposed)
        if refusal is not None:
            return refusal

        core_fields = ["instrument", "entry_intent", "size", "max_loss", "invalidation", "time_constraint"]
        for k in core_fields:
            if commit.get(k) != proposed.get(k):
                # Must contain substring "proposal_drift_requires_recommit" per tests
                return _out(HatDecision.REQUIRE_RECOMMIT, [REASON_RECOMMIT + ":" + str(k)], [], "RECOMMIT_REQUIRED")

        # Identical commit => allow with empty reasons (tests assert exactly []).
        return _out(HatDecision.ALLOW, [], [], "ALLOW")
