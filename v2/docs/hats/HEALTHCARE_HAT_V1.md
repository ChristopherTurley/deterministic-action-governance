# Healthcare Hat v1 (FROZEN)

STATUS
- Hat ID: HEALTHCARE_HAT_V1
- Authority: NONE
- Execution: NONE
- Advisory: NONE (refusal-only safety semantics)

PREFIX CONTRACT (LOCKED)
All refusal / recommit reasons MUST start with:
- INV_HEALTH_

INPUT CONTRACT (LOCKED)
Context keys:
- org_mode (admin | clinical)  [classification only]
- restricted_mode (bool)
- context_as_of_ts
- context_ttl_seconds

Proposal keys:
- request_type (admin | clinical)
- topic (string)
- now_ts
- summary

SEMANTICS
- PROPOSE:
  - fail-closed on missing/stale context
  - refuse clinical advice / diagnosis / prescribing requests
  - restricted_mode blocks sensitive health-data topics
  - allow admin/operational topics only
- COMMIT:
  - refuse if proposal not allowed
  - require recommit on drift
  - allow only if identical and proposal allowed

REASON TOKENS (PREFIXED)
- INV_HEALTH_missing_context_keys:<key>
- INV_HEALTH_context_stale
- INV_HEALTH_clinical_advice_or_diagnosis_disallowed
- INV_HEALTH_restricted_mode_blocks_sensitive_health_data
- INV_HEALTH_proposal_not_allowed
- INV_HEALTH_proposal_drift_requires_recommit:<keys>
- INV_HEALTH_malformed_input
- INV_HEALTH_malformed_proposal:<key>
- INV_HEALTH_malformed_timestamps
- INV_HEALTH_malformed_request_fields
