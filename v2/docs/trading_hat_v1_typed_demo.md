# Trading Hat v1 — Typed Demo (Copy/Paste)

## Manual open session (JSON mode)

Run:
PYTHONPATH=. python3 v2/demo/trading_open_session.py

When prompted `context_json>` paste this single JSON line:
{"instrument":"QQQ","time_of_day":"OPEN","volatility_state":"HIGH","liquidity_state":"GOOD","max_daily_loss":500,"daily_loss":0,"trades_taken_today":0,"trade_count_cap":3,"context_ttl_seconds":600}

When prompted `proposal_json>` paste this single JSON line:
{"instrument":"QQQ","entry_intent":"break and reclaim level","size":10,"max_loss":100,"invalidation":"level fails","time_constraint":"within 2 minutes"}

Then type:
commit

When prompted again `proposal_json>` paste the same line for ALLOW/ALLOW, or change size to 11 to force REQUIRE_RECOMMIT.
