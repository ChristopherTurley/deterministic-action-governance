# Hat Reason Codes Registry v1 (CANONICAL)

This registry is procurement-facing and exists to make refusal/recommit reason codes auditable.
It is **governance-only**: codes describe *boundaries*, not execution or advice.

## Invariant
- All non-ALLOW reasons MUST start with an `INV_*` prefix.
- Prefixes are declared by the canonical HATS invariant list in:
  - `v2/tests/test_domain_hats_registered_fail_closed_v1.py`

## Prefix Families (LOCKED)
The following prefix families are authoritative for Commercial Bundle v1 hats and stubs.

- `INV_OPS_`  (used by: OPS_INCIDENT_HAT_V1)
- `INV_PLATFORM_`  (used by: PLATFORM_ASSISTANTS_LENS_V1)
- `INV_EDU_`  (used by: EDUCATION_HAT_V1)
- `INV_HEALTH_`  (used by: HEALTHCARE_HAT_V1)
- `INV_SPORTS_`  (used by: COMPETITIVE_SPORTS_HAT_V1)
- `INV_EXEC_`  (used by: EXECUTIVE_HAT_V1)
- `INV_FOCUS_`  (used by: HIGH_FOCUS_WORKER_HAT_V1)
- `INV_DESIGN_`  (used by: DESIGNER_HAT_V1)
- `INV_ENG_`  (used by: ENGINEER_HAT_V1)

## Token Shape
Within a prefix family, tokens must be stable, deterministic, and machine-auditable, e.g.:
- `INV_TRD_missing_context_keys:max_daily_loss`
- `INV_EXEC_missing_context_keys:role`
- `INV_OPS_incident_mode_blocks_risky_ops`

## Source of Truth
- Runtime enforcement: `v2/hats/reason_allowlists_v1.py`
- Last regenerated: 2026-01-18 (UTC)

