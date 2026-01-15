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


def _line(msg: str) -> None:
    print(msg)


def _header(title: str) -> None:
    _line("")
    _line("================================================================")
    _line(title)
    _line("================================================================")


def _outcome(stage: str, outcome) -> None:
    _line(f"[{stage}]")
    _line(f"decision: {outcome.decision.value}")
    if outcome.reasons:
        _line("reasons:")
        for r in outcome.reasons:
            _line(f" - {r}")
    else:
        _line("reasons: (none)")
    _line(f"proposal_fingerprint: {outcome.proposal_fingerprint}")


def main() -> None:
    hat = TradingHatV1()

    _header("SCENARIO A — ALLOWED (PROPOSE + COMMIT)")
    ctx = base_context()
    proposed = base_proposal()
    _outcome("PROPOSE", hat.decide_proposal(ctx, proposed))
    _outcome("COMMIT", hat.decide_commit(ctx, proposed, deepcopy(proposed)))

    _header("SCENARIO B — REFUSED (RISK LIMIT)")
    ctx_risk = base_context()
    ctx_risk["daily_loss"] = 500.0
    _outcome("PROPOSE", hat.decide_proposal(ctx_risk, base_proposal()))

    _header("SCENARIO C — REQUIRE RE-COMMIT (COMMIT DRIFT)")
    ctx_ok = base_context()
    proposed2 = base_proposal()
    commit2 = deepcopy(proposed2)
    commit2["size"] = 2
    _outcome("COMMIT", hat.decide_commit(ctx_ok, proposed2, commit2))


if __name__ == "__main__":
    main()
