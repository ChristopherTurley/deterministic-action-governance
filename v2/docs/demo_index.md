# VERA v2 Demo Index (LOCKED SURFACES)

This folder contains operator-facing, versioned demo artifacts.
These demos do not change runtime behavior.

Core rule:
- VERA v1 remains locked and unchanged.
- v2 work is additive, modular, and fail-closed.

---

## One-command demo runner

Run everything (tests + all demos):
- `v2/demo/scripts/run_all_demos.sh`

---

## Trading Hat v1

### Week 2 — Deterministic Harness (3 scenarios)
Run:
- `./demo_trading_hat_v1.sh`

Scenarios:
- ALLOW (propose + commit)
- REFUSE (risk)
- REQUIRE_RECOMMIT (commit drift)

### Week 3 — Open Session (interactive)
Run:
- `PYTHONPATH=. python3 v2/demo/trading_open_session.py`

Copy/paste guide:
- `v2/docs/trading_hat_v1_typed_demo.md`

Verbal script + checklist:
- `v2/docs/trading_hat_v1_demo.md`

### Week 3 — Quick Live Demo (non-interactive)
Run:
- `./demo_trading_live_quick.sh`

### Spoken Demo Runner (opt-in voice, v1 untouched)
Run:
- `PYTHONPATH=. python3 v2/demo/trading_live_spoken_demo.py`

---

## Focus Hat v1 (Second Hat)

Run:
- `v2/demo/scripts/demo_focus_hat_v1.sh`

Docs:
- `v2/docs/focus_hat_v1_demo.md`

---

## Multi-hat Coexistence (Router v1)

Explicit selection only (no guessing).
Run:
- `v2/demo/scripts/demo_multi_hat_router_v1.sh`

---

## Coat v1 (Stable Decision Rendering)

Reason → message templates with snapshot tests (anti-drift).
Run:
- `v2/demo/scripts/demo_coat_v1.sh`

Docs:
- `v2/docs/coat_v1.md`

---

## Bridge v1 (Opt-in CLI, v1 unchanged)

Run Trading (drift -> REQUIRE_RECOMMIT):
- `v2/demo/scripts/demo_bridge_trading_hat.sh`

Run Focus (drift -> REQUIRE_RECOMMIT):
- `v2/demo/scripts/demo_bridge_focus_hat.sh`

Docs:
- `v2/docs/bridge_v1.md`
