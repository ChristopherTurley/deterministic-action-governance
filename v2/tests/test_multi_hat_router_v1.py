from v2.hats.router_v1 import route_proposal, route_commit


def test_unknown_hat_refuses():
    e = route_proposal("NOPE", {}, {})
    assert e["decision"] == "REFUSE"
    assert "unknown_hat:NOPE" in e["reasons"]


def test_focus_hat_routes_and_drifts():
    ctx = {
        "focus_mode": "DEEP_WORK",
        "context_as_of_ts": 1000,
        "context_ttl_seconds": 600,
        "task_count_cap": 5,
        "tasks_remaining": 3,
        "minutes_cap": 60,
        "minutes_remaining": 45,
    }
    proposed = {"task_count": 2, "planned_minutes": 30, "now_ts": 1100}
    commit = {"task_count": 3, "planned_minutes": 30, "now_ts": 1101}
    e1 = route_proposal("FOCUS_HAT_V1", ctx, proposed)
    assert e1["decision"] in ["ALLOW", "REFUSE", "REQUIRE_RECOMMIT"]
    e2 = route_commit("FOCUS_HAT_V1", ctx, proposed, commit)
    assert e2["decision"] == "REQUIRE_RECOMMIT"


def test_trading_hat_routes_allow():
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
    proposed = {
        "instrument": "QQQ",
        "entry_intent": "x",
        "size": 1,
        "max_loss": 10.0,
        "invalidation": "y",
        "time_constraint": "z",
        "now_ts": 1100,
    }
    commit = dict(proposed)
    e1 = route_proposal("TRADING_HAT_V1", ctx, proposed)
    assert e1["decision"] == "ALLOW"
    e2 = route_commit("TRADING_HAT_V1", ctx, proposed, commit)
    assert e2["decision"] == "ALLOW"
