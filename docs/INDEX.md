# Documentation Index

This index is an engineer-first map of the repository documents.

---

## Start here

1) Constitution and non-goals
- `docs/invariants.md`
- `docs/vera_will_never.md`

2) Refusal and failure semantics
- `docs/refusal_model.md`
- `docs/failure_modes.md`

3) Threat and security review
- `docs/threat_model.md`
- `docs/security_review_internal.md`

---

## Month 12: external intelligibility

- `docs/apple_gap_mapping.md`
  Neutral platform gap framing, oriented to what current frameworks do not express safely.

- `docs/demo_harness_walkthrough.md`
  Walkthrough for deterministic demonstration, if demo harness exists in this repo.

---

## Month 13: observability without control

- `docs/ledger_timeline_model.md`
  Proposal → decision → commit timeline clarity.

- `docs/drift_explanation_model.md`
  Drift definitions and how to describe drift without adding control.

- `docs/context_ttl_model.md`
  Context TTL visibility model and refusal expectations.

---

## Month 14: integration readiness

- `docs/integration_contract_v1.md`
  Integration contract and boundaries. VERA does not own execution.

- `docs/embedding_examples.md`
  Conceptual examples of embedding without SDK bloat.

- `docs/ownership_boundaries.md`
  What VERA does not own to prevent misuse.

---

## Month 15: positioning and safe scale paths

- `docs/allowed_expansions.md`
  Whitelist of power-neutral expansions.

- `docs/forbidden_expansions.md`
  Hard red lines that remain disallowed.

- `docs/future_governance_directions.md`
  Future direction ideas separated from current guarantees.

---

## Hats

- `docs/hats/reflection_hat_v1.md`
- `docs/hats/README.md`
  Hat system overview and usage.

- `docs/hats/hat_reason_codes_registry_v1.md`
  Canonical hat reason codes registry.

- Domain hats
  - `docs/hats/trading_hat_v1.md`
  - `docs/hats/ops_incident_hat_v1.md`
  - `docs/hats/platform_assistants_lens_v1.md`
  - `docs/hats/education_hat_v1.md`
  - `docs/hats/healthcare_hat_v1.md`
  - `docs/hats/competitive_sports_hat_v1.md`
  - `docs/hats/executive_hat_v1.md`
  - `docs/hats/high_focus_worker_hat_v1.md`
  - `docs/hats/designer_hat_v1.md`
  - `docs/hats/engineer_hat_v1.md`

## Coats
- `docs/coats/refusal_coat_v1.md`

---

## Reading guidance

If you are evaluating safety and control:
- start with invariants, refusal model, failure modes, and threat model

If you are evaluating adoption and integration:
- start with integration contract and ownership boundaries

If you are evaluating whether this is an agent:
- start with invariants and refusal model
