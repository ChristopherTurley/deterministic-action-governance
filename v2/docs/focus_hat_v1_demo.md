# Focus Hat v1 — Demo (v1.0)

Purpose:
Deterministic enforcement of focus/session constraints (no strategy, no autonomy).

Run:
- `./demo_focus_hat_v1.sh`

Scenarios:
- ALLOW (propose + commit)
- REFUSE (task cap exceeded)
- REQUIRE_RECOMMIT (commit drift)

Key guarantees:
- context TTL enforced
- proposal requires task_count
- optional planned_minutes enforced if present
- drift on protected fields forces recommit
- audit ledger events emitted
