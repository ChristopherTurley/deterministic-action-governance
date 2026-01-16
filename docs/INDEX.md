# VERA — Documentation Index (Navigation Spine)

This index defines **what is canonical** vs **what is informative**.
Governance requires explicit authority. This file provides it.

## Canonical (Normative)

These define governance semantics and boundaries.

- `docs/START_HERE.md`
- `docs/REFERENCE_FREEZE.md`
- `docs/vera_will_never.md`
- `docs/invariants.md`
- `docs/refusal_model.md`
- `docs/threat_model.md`

Canonical spec tied to code + tests:
- `v2/docs/` (wins in conflicts with `docs/`)

Enforcement:
- `v2/tests/` (final enforcement layer)

## Public Evaluation Pack (Skeptic Onramp)

- `v2/docs/public/README_PUBLIC.md`
- `v2/docs/public/ONE_PAGER.md`
- `v2/docs/public/DEMO_SCRIPT_VERBAL.md`
- `v2/docs/public/MONTH12_PUBLIC_ARTIFACT_LOCK.md`

## Informative (Non-Normative)

These explain concepts without changing authority.

### Hats (Domain Decision Layers, Not Capabilities)

- `docs/hats/README.md`
- Domain hats in `docs/hats/*.md`

### Coats (Explanation-Only Rendering, Non-Decisional)

- `docs/coats/*`

### Governance Models and Long-Run Architecture

- `docs/context_ttl_model.md`
- `docs/drift_explanation_model.md`
- `docs/ledger_timeline_model.md`
- `docs/integration_contract_v1.md`
- `docs/ownership_boundaries.md`
- `docs/failure_modes.md`
- `docs/allowed_expansions.md`
- `docs/forbidden_expansions.md`

### Platform Framing (Pressure Lane)

- `docs/platform_gaps/*`
- `docs/platform_framing.md`
- `docs/pressure_narrative.md`

## Private-Only Material

Anything under `docs/private/` is intentionally segregated and not part of the public evaluation surface.
