#!/bin/sh
set -eu
cd "$(dirname "$0")/../.."
PYTHONPATH=. python3 v2/bridge/run_hat_session.py \
  --hat TRADING_HAT_V1 \
  --context '{"instrument":"QQQ","time_of_day":"OPEN","volatility_state":"HIGH","liquidity_state":"GOOD","max_daily_loss":500,"daily_loss":0,"trades_taken_today":0,"trade_count_cap":3,"context_ttl_seconds":600}' \
  --proposal '{"instrument":"QQQ","entry_intent":"break and reclaim level","size":10,"max_loss":100,"invalidation":"level fails","time_constraint":"within 2 minutes"}' \
  --commit '{"instrument":"QQQ","entry_intent":"break and reclaim level","size":11,"max_loss":100,"invalidation":"level fails","time_constraint":"within 2 minutes"}'
