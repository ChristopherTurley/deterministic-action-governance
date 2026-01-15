# VERA v2 Demo Index (LOCKED SURFACES)

This folder contains operator-facing, versioned demo artifacts.
These docs do not change runtime behavior.

## Trading Hat v1

### Week 2 — Deterministic Harness (3 scenarios)
Run:
- `./demo_trading_hat_v1.sh`

Scenarios:
- ALLOW (propose + commit)
- REFUSE (risk)
- REQUIRE_RECOMMIT (commit drift)

### Week 3 — Live Open Session (interactive)
Run:
- `PYTHONPATH=. python3 v2/demo/trading_open_session.py`

For copy/paste JSON and expected outcomes, see:
- `trading_hat_v1_typed_demo.md`

For the verbal script + checklist, see:
- `trading_hat_v1_demo.md`

## Notes
- v1 remains locked and unchanged.
- All demo paths are opt-in and terminal-based.
