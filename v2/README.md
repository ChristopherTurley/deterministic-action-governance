# VERA v2 — Execution Substrate Boundary (v1 LOCKED)

## Non-negotiable
- v1 is read-only in v2 work. No behavior changes. No refactors.
- v2 adds a boundary layer + test vectors to protect State / Continuity / Trust.

## What exists in v2 (so far)
- schema.json: EngineInput / EngineOutput + Persistent Daily State (PDS)
- reducer_rules.md: canonical state rules (human-readable)
- state_reducer.py: minimal reducer stub (deterministic)
- tests/: headless runner + golden vectors (added next)

## Run tests
- python3 v2/tests/run_tests.py

## Revert (remove v2 entirely)
- rm -rf v2
