# Trading Hat v1 Rules (v1)

This is a human-readable rule index. Runtime truth is enforced by tests.

## Context Requirements (PROPOSE)
Refuse if:
- context missing required keys
- context is stale (now_ts - context_as_of_ts > context_ttl_seconds)

## Risk Rules (PROPOSE)
Refuse if:
- daily_loss >= max_daily_loss

## Trade Count Rules (PROPOSE)
Refuse if:
- trades_taken_today >= trade_count_cap

## Proposal Requirements (PROPOSE)
Refuse if proposal missing:
- max_loss
- invalidation
- size
- entry_intent
- time_constraint

## Commit Drift Rules (COMMIT)
Require re-commit if commit deviates from proposed in protected fields:
- size
- entry intent
- max loss
- invalidation
(Exact protected fields are defined by Trading Hat v1 and locked by tests.)

## Notes
- No strategy generation and no prediction.
- Decisions are deterministic and audit-logged.
