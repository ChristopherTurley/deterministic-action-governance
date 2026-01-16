# Phase 11 — Narrative Lock (Public)

Purpose
Freeze the public-facing meaning of this repository so:
- evaluators get a stable reference target
- future changes cannot rewrite history
- citations remain valid over time

Locked claims
- This repo is governance-only
- No background behavior
- No side effects without explicit operator commit
- Refusal and inaction are correct outcomes
- Determinism is enforced by tests
- Hats and coats are governance layers
- Stubbed hats are explicit refusals by design
- Execution adapters and integrations do not live here

Canonical evaluation path
- docs/START_HERE.md
- pytest -q

Non-goals
- product UI
- automation
- external service execution

Change rule
Any change that alters the locked claims must:
- be explicitly declared
- be guarded by tests
- receive a new narrative-lock tag
