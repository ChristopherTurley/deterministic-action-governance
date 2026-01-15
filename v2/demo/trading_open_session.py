from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from v2.hats.trading_hat_v1 import TradingHatV1
from v2.hats.hat_interface import HatDecision


@dataclass
class SessionEvent:
    ts: int
    type: str
    payload: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {"ts": self.ts, "type": self.type, "payload": self.payload}


def _now_ts() -> int:
    return int(time.time())


def _print_title(msg: str) -> None:
    print("")
    print("================================================================")
    print(msg)
    print("================================================================")


def _prompt(msg: str) -> str:
    return input(msg).strip()


def _prompt_float(label: str) -> float:
    while True:
        raw = _prompt(f"{label}: ")
        try:
            return float(raw)
        except Exception:
            print("Invalid number. Try again.")


def _prompt_int(label: str) -> int:
    while True:
        raw = _prompt(f"{label}: ")
        try:
            return int(raw)
        except Exception:
            print("Invalid integer. Try again.")


def _prompt_text(label: str, allow_empty: bool = False) -> str:
    while True:
        raw = _prompt(f"{label}: ")
        if raw == "" and not allow_empty:
            print("Cannot be empty. Try again.")
            continue
        return raw


def _print_outcome(outcome) -> None:
    print("")
    print(f"DECISION: {outcome.decision.value}")
    if outcome.reasons:
        print("REASONS:")
        for r in outcome.reasons:
            print(" -", r)
    else:
        print("REASONS: (none)")
    print("FINGERPRINT:", outcome.proposal_fingerprint)


def _print_protocol_reminder() -> None:
    print("")
    print("Protocol:")
    print(" - This session never predicts direction.")
    print(" - It only returns ALLOW / REFUSE / REQUIRE_RECOMMIT.")
    print(" - Nothing executes automatically.")
    print(" - You must type COMMIT to proceed (case-insensitive).")
    print(" - JSON paste mode is supported for context/proposal/commit.")
    print("")


def _try_parse_json(raw: str) -> Optional[Dict[str, Any]]:
    raw = raw.strip()
    if raw == "":
        return None
    try:
        obj = json.loads(raw)
        if not isinstance(obj, dict):
            return None
        return obj
    except Exception:
        return None


def _require_keys(obj: Dict[str, Any], required: List[str]) -> List[str]:
    missing: List[str] = []
    for k in required:
        if k not in obj or obj.get(k) is None:
            missing.append(k)
    return missing


def _context_from_json(obj: Dict[str, Any]) -> Dict[str, Any]:
    # Normalize and coerce types where needed.
    now = _now_ts()
    return {
        "instrument": str(obj["instrument"]),
        "time_of_day": str(obj["time_of_day"]),
        "volatility_state": str(obj["volatility_state"]),
        "liquidity_state": str(obj["liquidity_state"]),
        "max_daily_loss": float(obj["max_daily_loss"]),
        "daily_loss": float(obj["daily_loss"]),
        "trades_taken_today": int(obj["trades_taken_today"]),
        "trade_count_cap": int(obj["trade_count_cap"]),
        "context_as_of_ts": int(obj.get("context_as_of_ts", now)),
        "context_ttl_seconds": int(obj["context_ttl_seconds"]),
    }


def _proposal_from_json(obj: Dict[str, Any], default_instrument: str) -> Dict[str, Any]:
    now = _now_ts()
    instrument = str(obj.get("instrument", default_instrument))
    return {
        "instrument": instrument,
        "entry_intent": str(obj["entry_intent"]),
        "size": float(obj["size"]),
        "max_loss": float(obj["max_loss"]),
        "invalidation": str(obj["invalidation"]),
        "time_constraint": str(obj["time_constraint"]),
        "now_ts": int(obj.get("now_ts", now)),
    }


def _build_context() -> Dict[str, Any]:
    _print_title("TRADING SESSION — CONTEXT SNAPSHOT (DECLARED, READ-ONLY)")

    print("Paste JSON for context, or press Enter for manual entry.")
    raw = _prompt("context_json> ")
    obj = _try_parse_json(raw)

    required = [
        "instrument",
        "time_of_day",
        "volatility_state",
        "liquidity_state",
        "max_daily_loss",
        "daily_loss",
        "trades_taken_today",
        "trade_count_cap",
        "context_ttl_seconds",
    ]

    if obj is not None:
        missing = _require_keys(obj, required)
        if missing:
            print("Missing keys in context JSON:", ",".join(sorted(missing)))
            print("Falling back to manual entry.")
        else:
            return _context_from_json(obj)

    instrument = _prompt_text("instrument (e.g., SPX/QQQ)")
    time_of_day = _prompt_text("time_of_day (e.g., OPEN/MID/CLOSE)")
    volatility_state = _prompt_text("volatility_state (declared)")
    liquidity_state = _prompt_text("liquidity_state (declared)")
    max_daily_loss = _prompt_float("max_daily_loss")
    daily_loss = _prompt_float("daily_loss (so far today)")
    trades_taken_today = _prompt_int("trades_taken_today")
    trade_count_cap = _prompt_int("trade_count_cap")
    ttl = _prompt_int("context_ttl_seconds (stale if exceeded)")

    now = _now_ts()
    return {
        "instrument": instrument,
        "time_of_day": time_of_day,
        "volatility_state": volatility_state,
        "liquidity_state": liquidity_state,
        "max_daily_loss": max_daily_loss,
        "daily_loss": daily_loss,
        "trades_taken_today": trades_taken_today,
        "trade_count_cap": trade_count_cap,
        "context_as_of_ts": now,
        "context_ttl_seconds": ttl,
    }


def _build_proposal(default_instrument: str, title: str) -> Dict[str, Any]:
    _print_title(title)

    print("Paste JSON for proposal, or type 'manual' for manual entry.")
    while True:
        raw = _prompt("proposal_json> ")
        if raw.strip().lower() == "manual" or raw.strip() == "":
            break

        obj = _try_parse_json(raw)
        if obj is None:
            print("Invalid JSON. Paste a single JSON object, or type 'manual'.")
            continue

        # Guard: detect context-like JSON mistakenly pasted here
        contextish_keys = {"time_of_day", "volatility_state", "liquidity_state", "trade_count_cap", "context_ttl_seconds"}
        if any(k in obj for k in contextish_keys):
            print("You pasted CONTEXT JSON into the PROPOSAL prompt. Paste proposal JSON (entry_intent/size/max_loss/invalidation/time_constraint).")
            continue

        required = ["entry_intent", "size", "max_loss", "invalidation", "time_constraint"]
        missing = _require_keys(obj, required)
        if missing:
            print("Missing keys in proposal JSON:", ",".join(sorted(missing)))
            continue

        return _proposal_from_json(obj, default_instrument=default_instrument)

    entry_intent = _prompt_text("entry_intent (plain text ok)")
    size = _prompt_float("size (contracts/shares)")
    max_loss = _prompt_float("max_loss (dollars)")
    invalidation = _prompt_text("invalidation (plain text ok)")
    time_constraint = _prompt_text("time_constraint (plain text ok)")
    now = _now_ts()
    return {
        "instrument": default_instrument,
        "entry_intent": entry_intent,
        "size": size,
        "max_loss": max_loss,
        "invalidation": invalidation,
        "time_constraint": time_constraint,
        "now_ts": now,
    }


def main() -> None:
    hat = TradingHatV1()
    events: List[SessionEvent] = []

    _print_title("TRADING HAT v1 — OPEN SESSION (PAPER / MICRO ONLY)")
    _print_protocol_reminder()

    ctx = _build_context()
    events.append(SessionEvent(ts=_now_ts(), type="TRADING_CONTEXT", payload=dict(ctx)))

    # Proposal stage
    proposal = _build_proposal(default_instrument=str(ctx["instrument"]), title="PROPOSAL (NO STRATEGY — MECHANICAL FIELDS ONLY)")
    events.append(SessionEvent(ts=_now_ts(), type="TRADING_PROPOSAL", payload=dict(proposal)))

    out_prop = hat.decide_proposal(ctx, proposal)
    events.append(SessionEvent(ts=_now_ts(), type="HAT_DECISION", payload=out_prop.to_ledger_event()))
    _print_outcome(out_prop)

    if out_prop.decision == HatDecision.REFUSE:
        _print_title("SESSION END — REFUSED AT PROPOSAL STAGE")
        _emit_ledger(events)
        return

    # Commit stage
    print("")
    print("To commit, type: COMMIT (case-insensitive)")
    print("To abort, type: ABORT")
    cmd = _prompt("> ")

    if cmd.strip().upper() != "COMMIT":
        _print_title("SESSION END — ABORTED")
        events.append(SessionEvent(ts=_now_ts(), type="SESSION_ABORT", payload={"reason": "operator_abort"}))
        _emit_ledger(events)
        return

    commit = _build_proposal(default_instrument=str(ctx["instrument"]), title="COMMIT INPUT (REPEAT PROPOSAL — CHANGES REQUIRE RE-COMMIT)")
    events.append(SessionEvent(ts=_now_ts(), type="TRADING_COMMIT", payload=dict(commit)))

    out_commit = hat.decide_commit(ctx, proposal, commit)
    events.append(SessionEvent(ts=_now_ts(), type="HAT_DECISION", payload=out_commit.to_ledger_event()))
    _print_outcome(out_commit)

    if out_commit.decision == HatDecision.REQUIRE_RECOMMIT:
        _print_title("SESSION END — REQUIRE RE-COMMIT (NO SILENT DRIFT)")
        _emit_ledger(events)
        return

    if out_commit.decision == HatDecision.REFUSE:
        _print_title("SESSION END — REFUSED AT COMMIT STAGE")
        _emit_ledger(events)
        return

    _print_title("SESSION END — ALLOWED (EXECUTION STILL MANUAL)")
    print("Reminder: VERA does not execute trades. This only proves governance.")
    _emit_ledger(events)


def _emit_ledger(events: List[SessionEvent]) -> None:
    print("")
    print("================================================================")
    print("LEDGER (AUDIT OUTPUT)")
    print("================================================================")
    blob = [e.to_dict() for e in events]
    print(json.dumps(blob, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
