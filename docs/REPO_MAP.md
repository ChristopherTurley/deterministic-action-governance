# VERA — Repo Map (Structural)

This is the structural inventory of the repository, with explicit authority.

## Top-Level Authority Rules

- `docs/` contains conceptual, narrative, and cross-domain governance material.
- `v2/docs/` contains **canonical specifications** whose claims are enforced by tests.
- In case of conflict: **tests win**, then `v2/docs/`, then `docs/`.

## Key Paths

- `docs/START_HERE.md` — intended evaluator onramp
- `docs/INDEX.md` — navigation spine
- `docs/REFERENCE_FREEZE.md` — immutability posture
- `docs/vera_will_never.md` — forbidden behaviors (hard boundary)
- `docs/invariants.md` + `docs/threat_model.md` + `docs/refusal_model.md` — governing semantics

## Hats + Coats

- `docs/hats/` — domain lenses (non-capability)
- `docs/coats/` — explanation-only rendering (non-decisional)

## Canonical Implementation Lane

- `v2/` — canonical governance implementation, spec, demos, and tests
- `v2/docs/` — canonical spec tied to tests
- `v2/tests/` — enforcement spine

## Public Evaluation Pack

- `v2/docs/public/` — skeptic bundle intended for third-party review

## Hygiene

Generated artifacts must not be committed:
- `__pycache__/`
- `*.pyc`
- local OS noise files

## Ignored generated artifacts
These artifacts are local-only and should not be treated as repo surfaces:
- `__pycache__/`
- `*.pyc`
- `.pytest_cache/`

