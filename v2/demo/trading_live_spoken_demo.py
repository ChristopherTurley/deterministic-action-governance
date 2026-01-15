from __future__ import annotations

import json
import subprocess
import sys
from typing import List

from v2.hats.trading_hat_v1 import TradingHatV1
from v2.hats.hat_interface import HatDecision


def _say(text: str) -> None:
    # macOS built-in TTS. No dependency on v1 runtime.
    try:
        subprocess.run(["say", text], check=False)
    except Exception:
        pass


def _print(title: str) -> None:
    print("")
    print("================================================================")
    print(title)
    print("================================================================")


def run_scenario(title: str, ctx: dict, proposal: dict, commit: dict) -> None:
    hat = TradingHatV1()

    _print(title)
    out_p = hat.decide_proposal(ctx, proposal)
    print("PROPOSE:", out_p.decision.value, out_p.reasons)
    _say(f"Proposal decision: {out_p.decision.value}")

    if out_p.decision == HatDecision.REFUSE:
        if out_p.reasons:
            _say("Reason: " + ", ".join(out_p.reasons))
        return

    out_c = hat.decide_commit(ctx, proposal, commit)
    print("COMMIT:", out_c.decision.value, out_c.reasons)
    _say(f"Commit decision: {out_c.decision.value}")
    if out_c.reasons:
        _say("Reason: " + ", ".join(out_c.reasons))


def main() -> None:
    ctx = {
        "instrument": "QQQ",
        "time_of_day": "OPEN",
        "volatility_state": "HIGH",
        "liquidity_state": "GOOD",
        "max_daily_loss": 500.0,
        "daily_loss": 0.0,
        "trades_taken_today": 0,
        "trade_count_cap": 3,
        "context_as_of_ts": 1000,
        "context_ttl_seconds": 600,
    }

    proposal = {
        "instrument": "QQQ",
        "entry_intent": "break and reclaim level",
        "size": 10,
        "max_loss": 100.0,
        "invalidation": "level fails",
        "time_constraint": "within 2 minutes",
        "now_ts": 1100,
    }

    commit_same = dict(proposal)
    commit_drift = dict(proposal)
    commit_drift["size"] = 11

    _say("Starting Trading Hat live demo.")
    _say("This does not predict markets. It only enforces allow, refuse, or require re-commit.")

    run_scenario("SCENARIO A — ALLOW / ALLOW", ctx, proposal, commit_same)
    run_scenario("SCENARIO C — DRIFT / REQUIRE RE-COMMIT", ctx, proposal, commit_drift)

    _say("Demo complete.")
    _say("VERA doesn't help me win trades. It prevents me from breaking my rules.")


if __name__ == "__main__":
    main()
