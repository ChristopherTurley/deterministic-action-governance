# Healthcare Hat v1 — Governance Specification

Status: Draft v1
Scope: Governance-only
Power: Zero

## Purpose
Make authority explicit in clinical/healthcare workflows without providing medical advice.

Never:
- diagnosis
- treatment recommendations
- medical device behavior
- patient monitoring

No patient data is required for the governance model.

## Domain Declaration (Vocabulary Only)
- RECORD_DECISION
- REQUEST_POLICY_BOUNDARY
- REQUIRE_CLINICIAN_COMMIT
- DECLARE_CLINICAL_CONSTRAINTS

## Invariants (Refusal-Only)
category=INVARIANT. Reason codes:
- INV_HEALTH_NO_DIAGNOSIS
- INV_HEALTH_NO_TREATMENT_RECOMMENDATION
- INV_HEALTH_CLINICIAN_AUTHORITY_REQUIRED
- INV_HEALTH_MISSING_REQUIRED_CONTEXT
