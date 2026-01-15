from __future__ import annotations

import json

from v2.coat.coat_v1 import render_hat_event
from v2.hats.router_v1 import route_proposal, route_commit


def _banner(t: str) -> None:
    print("")
    print("================================================================")
    print(t)
    print("================================================================")


def main() -> None:
    # Trading: allow
    trading_ctx = {
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
    trading_prop = {
        "instrument": "QQQ",
        "entry_intent": "x",
        "size": 1,
        "max_loss": 10.0,
        "invalidation": "y",
        "time_constraint": "z",
        "now_ts": 1100,
    }
    trading_commit = dict(trading_prop)

    _banner("TRADING — ALLOW/ALLOW (COATED)")
    e1 = route_proposal("TRADING_HAT_V1", trading_ctx, trading_prop)
    e2 = route_commit("TRADING_HAT_V1", trading_ctx, trading_prop, trading_commit)
    print(render_hat_event(e1)["display"])
    print("")
    print(render_hat_event(e2)["display"])

    # Focus: drift
    focus_ctx = {
        "focus_mode": "DEEP_WORK",
        "context_as_of_ts": 1000,
        "context_ttl_seconds": 600,
        "task_count_cap": 5,
        "tasks_remaining": 3,
        "minutes_cap": 60,
        "minutes_remaining": 45,
    }
    focus_prop = {"task_count": 2, "planned_minutes": 30, "now_ts": 1100}
    focus_commit_drift = {"task_count": 3, "planned_minutes": 30, "now_ts": 1101}

    _banner("FOCUS — DRIFT (COATED)")
    e3 = route_commit("FOCUS_HAT_V1", focus_ctx, focus_prop, focus_commit_drift)
    print(render_hat_event(e3)["display"])

    # Unknown hat
    _banner("UNKNOWN HAT — REFUSE (COATED)")
    e4 = route_proposal("NOPE", {}, {})
    print(render_hat_event(e4)["display"])


if __name__ == "__main__":
    main()
