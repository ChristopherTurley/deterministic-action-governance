from __future__ import annotations

from copy import deepcopy
from v2.hats.trading_hat_v1 import TradingHatV1

def base_context():
    return {
        "instrument": "SPX",
        "time_of_day": "OPEN",
        "volatility_state": "HIGH",
        "liquidity_state": "GOOD",
        "max_daily_loss": 500.0,
        "daily_loss": 0.0,
        "trades_taken_today": 0,
        "trade_count_cap": 3,
        "context_as_of_ts": 1000,
        "context_ttl_seconds": 300,
    }

def base_proposal():
    return {
        "instrument": "SPX",
        "entry_intent": "break and reclaim level",
        "size": 1,
        "max_loss": 100.0,
        "invalidation": "level fails",
        "time_constraint": "within 2 minutes",
        "now_ts": 1100,
    }

def print_outcome(title: str, outcome):
    print("")
    print("=== " + title + " ===")
    print("decision:", outcome.decision.value)
    if outcome.reasons:
        print("reasons:")
        for r in outcome.reasons:
            print(" -", r)
    else:
        print("reasons: (none)")
    print("ledger_event:", outcome.to_ledger_event())

def main():
    hat = TradingHatV1()

    # Scenario A: allowed proposal + allowed commit
    ctx = base_context()
    proposed = base_proposal()
    out_prop = hat.decide_proposal(ctx, proposed)
    print_outcome("SCENARIO A — PROPOSE", out_prop)

    out_commit = hat.decide_commit(ctx, proposed, deepcopy(proposed))
    print_outcome("SCENARIO A — COMMIT", out_commit)

    # Scenario B: refused (risk)
    ctx_risk = base_context()
    ctx_risk["daily_loss"] = 500.0
    out_risk = hat.decide_proposal(ctx_risk, base_proposal())
    print_outcome("SCENARIO B — REFUSE (RISK)", out_risk)

    # Scenario C: require re-commit (proposal drift at commit)
    ctx_ok = base_context()
    proposed2 = base_proposal()
    commit2 = deepcopy(proposed2)
    commit2["size"] = 2
    out_drift = hat.decide_commit(ctx_ok, proposed2, commit2)
    print_outcome("SCENARIO C — REQUIRE RE-COMMIT (DRIFT)", out_drift)

if __name__ == "__main__":
    main()
