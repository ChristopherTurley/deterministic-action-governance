from v2.hats.trading_hat_v1 import TradingHatV1
from v2.hats.hat_interface import HatDecision


def _base_context():
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


def _base_proposal():
    return {
        "instrument": "SPX",
        "entry_intent": "break and reclaim level",
        "size": 1,
        "max_loss": 100.0,
        "invalidation": "level fails",
        "time_constraint": "within 2 minutes",
        "now_ts": 1100,
    }


def test_missing_context_refuses_fail_closed():
    hat = TradingHatV1()
    ctx = _base_context()
    del ctx["max_daily_loss"]

    out = hat.decide_proposal(ctx, _base_proposal())
    assert out.decision == HatDecision.REFUSE
    assert any("missing_context_keys" in r for r in out.reasons)


def test_risk_limit_refuses():
    hat = TradingHatV1()
    ctx = _base_context()
    ctx["daily_loss"] = 500.0  # at limit => refuse
    out = hat.decide_proposal(ctx, _base_proposal())
    assert out.decision == HatDecision.REFUSE
    assert "risk_daily_loss_limit_reached_or_exceeded" in out.reasons


def test_trade_count_cap_refuses():
    hat = TradingHatV1()
    ctx = _base_context()
    ctx["trades_taken_today"] = 3  # at cap => refuse
    out = hat.decide_proposal(ctx, _base_proposal())
    assert out.decision == HatDecision.REFUSE
    assert "trade_count_cap_reached_or_exceeded" in out.reasons


def test_stale_context_refuses():
    hat = TradingHatV1()
    ctx = _base_context()
    # now_ts 1400 => age 400 > ttl 300 => stale
    prop = _base_proposal()
    prop["now_ts"] = 1400

    out = hat.decide_proposal(ctx, prop)
    assert out.decision == HatDecision.REFUSE
    assert "context_stale" in out.reasons


def test_commit_requires_recommit_if_size_changes():
    hat = TradingHatV1()
    ctx = _base_context()
    proposed = _base_proposal()
    commit = dict(proposed)
    commit["size"] = 2

    out = hat.decide_commit(ctx, proposed, commit)
    assert out.decision == HatDecision.REQUIRE_RECOMMIT
    assert any("proposal_drift_requires_recommit" in r for r in out.reasons)


def test_commit_requires_recommit_if_entry_changes():
    hat = TradingHatV1()
    ctx = _base_context()
    proposed = _base_proposal()
    commit = dict(proposed)
    commit["entry_intent"] = "different entry wording"

    out = hat.decide_commit(ctx, proposed, commit)
    assert out.decision == HatDecision.REQUIRE_RECOMMIT


def test_commit_allows_when_identical_and_constraints_ok():
    hat = TradingHatV1()
    ctx = _base_context()
    proposed = _base_proposal()
    commit = dict(proposed)

    out = hat.decide_commit(ctx, proposed, commit)
    assert out.decision == HatDecision.ALLOW
    assert out.reasons == []


def test_instrument_mismatch_refuses():
    hat = TradingHatV1()
    ctx = _base_context()
    prop = _base_proposal()
    prop["instrument"] = "QQQ"

    out = hat.decide_proposal(ctx, prop)
    assert out.decision == HatDecision.REFUSE
    assert "instrument_mismatch_with_context" in out.reasons
