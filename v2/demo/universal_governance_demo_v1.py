from __future__ import annotations

from typing import Any, Dict

from v2.hats.router_v1 import route_proposal, route_commit
from v2.coat.coat_v1 import render_decision_v1


def _banner(title: str) -> None:
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)


def _print_event(label: str, e: Dict[str, Any]) -> None:
    print(f"[{label}]")
    print(f"type: {e.get('type')}")
    print(f"hat: {e.get('hat')}")
    print(f"stage: {e.get('stage')}")
    print(f"decision: {e.get('decision')}")
    print("reasons:")
    for r in e.get("reasons", []):
        print(f" - {r}")
    print(f"proposal_fingerprint: {e.get('proposal_fingerprint')}")
    if "known_hats" in e:
        print(f"known_hats: {e.get('known_hats')}")
    display = render_decision_v1(e)
    print("coat_display:")
    for line in display.splitlines():
        print(f"  {line}")
    print("")


def main() -> None:
    # -----------------------
    # TRADING
    # -----------------------
    _banner("SCENARIO 1 — TRADING (ALLOW + DRIFT)")
    trading_ctx = {
        "instrument": "SPX",
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
    trading_proposed = {
        "instrument": "SPX",
        "entry_intent": "break of level",
        "size": 1,
        "max_loss": 100.0,
        "invalidation": "level fails",
        "time_constraint": "2m",
        "now_ts": 1100,
    }
    trading_commit_same = dict(trading_proposed)
    trading_commit_drift = dict(trading_proposed)
    trading_commit_drift["size"] = 2

    e1 = route_proposal("TRADING_HAT_V1", trading_ctx, trading_proposed)
    _print_event("PROPOSE", e1)
    e2 = route_commit("TRADING_HAT_V1", trading_ctx, trading_proposed, trading_commit_same)
    _print_event("COMMIT", e2)
    e3 = route_commit("TRADING_HAT_V1", trading_ctx, trading_proposed, trading_commit_drift)
    _print_event("COMMIT_DRIFT", e3)

    # -----------------------
    # FOCUS
    # -----------------------
    _banner("SCENARIO 2 — FOCUS (ALLOW + DRIFT)")
    focus_ctx = {
        "focus_mode": "DEEP_WORK",
        "context_as_of_ts": 2000,
        "context_ttl_seconds": 600,
        "task_count_cap": 5,
        "tasks_remaining": 3,
        "minutes_cap": 60,
        "minutes_remaining": 45,
    }
    focus_proposed = {"task_count": 2, "planned_minutes": 30, "now_ts": 2100}
    focus_commit_same = dict(focus_proposed)
    focus_commit_drift = dict(focus_proposed)
    focus_commit_drift["task_count"] = 3

    f1 = route_proposal("FOCUS_HAT_V1", focus_ctx, focus_proposed)
    _print_event("PROPOSE", f1)
    f2 = route_commit("FOCUS_HAT_V1", focus_ctx, focus_proposed, focus_commit_same)
    _print_event("COMMIT", f2)
    f3 = route_commit("FOCUS_HAT_V1", focus_ctx, focus_proposed, focus_commit_drift)
    _print_event("COMMIT_DRIFT", f3)

    # -----------------------
    # UNKNOWN HAT
    # -----------------------
    _banner("SCENARIO 3 — UNKNOWN HAT (FAIL-CLOSED)")
    u1 = route_proposal("NOT_A_REAL_HAT_V1", {"context_as_of_ts": 1, "context_ttl_seconds": 999999}, {"now_ts": 2})
    _print_event("PROPOSE", u1)
    u2 = route_commit("NOT_A_REAL_HAT_V1", {"context_as_of_ts": 1, "context_ttl_seconds": 999999}, {"now_ts": 2}, {"now_ts": 3})
    _print_event("COMMIT", u2)


if __name__ == "__main__":
    main()
