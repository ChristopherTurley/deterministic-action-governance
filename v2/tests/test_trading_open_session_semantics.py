from v2.hats.trading_hat_v1 import TradingHatV1
from v2.hats.hat_interface import HatDecision


def test_open_session_refuses_when_context_stale():
    hat = TradingHatV1()
    ctx = {
        "instrument": "SPX",
        "time_of_day": "OPEN",
        "volatility_state": "HIGH",
        "liquidity_state": "GOOD",
        "max_daily_loss": 500.0,
        "daily_loss": 0.0,
        "trades_taken_today": 0,
        "trade_count_cap": 3,
        "context_as_of_ts": 1000,
        "context_ttl_seconds": 10,
    }
    proposal = {
        "instrument": "SPX",
        "entry_intent": "x",
        "size": 1,
        "max_loss": 100.0,
        "invalidation": "y",
        "time_constraint": "z",
        "now_ts": 2000,  # stale
    }
    out = hat.decide_proposal(ctx, proposal)
    assert out.decision == HatDecision.REFUSE
    assert "context_stale" in out.reasons


def test_open_session_requires_recommit_on_commit_drift():
    hat = TradingHatV1()
    ctx = {
        "instrument": "SPX",
        "time_of_day": "OPEN",
        "volatility_state": "HIGH",
        "liquidity_state": "GOOD",
        "max_daily_loss": 500.0,
        "daily_loss": 0.0,
        "trades_taken_today": 0,
        "trade_count_cap": 3,
        "context_as_of_ts": 1000,
        "context_ttl_seconds": 3000,
    }
    proposed = {
        "instrument": "SPX",
        "entry_intent": "break",
        "size": 1,
        "max_loss": 100.0,
        "invalidation": "fail",
        "time_constraint": "2m",
        "now_ts": 1100,
    }
    commit = dict(proposed)
    commit["size"] = 2
    out = hat.decide_commit(ctx, proposed, commit)
    assert out.decision == HatDecision.REQUIRE_RECOMMIT
    assert any("proposal_drift_requires_recommit" in r for r in out.reasons)
