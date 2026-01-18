# Education Hat v1 (FROZEN)

STATUS
- Hat ID: EDUCATION_HAT_V1
- Authority: NONE
- Execution: NONE
- Advisory: NONE (refusal-only integrity semantics)

PREFIX CONTRACT (LOCKED)
All refusal / recommit reasons MUST start with:
- INV_EDU_

INPUT CONTRACT (LOCKED)
Context keys:
- role (student | teacher | admin) [classification only]
- assessment_mode (bool)
- context_as_of_ts
- context_ttl_seconds

Proposal keys:
- request_type (tutoring | answer_key | rewrite | test_help)
- topic (string)
- now_ts
- summary

SEMANTICS
- PROPOSE:
  - fail-closed on missing/stale context
  - refuse cheating / answer-key / do-my-work signals
  - assessment_mode blocks direct answers
  - allow tutoring-style support only
- COMMIT:
  - refuse if proposal not allowed
  - require recommit on drift
  - allow only if identical and proposal allowed

REASON TOKENS (PREFIXED)
- INV_EDU_missing_context_keys:<key>
- INV_EDU_context_stale
- INV_EDU_academic_integrity_violation_cheating_request
- INV_EDU_assessment_mode_blocks_direct_answers
- INV_EDU_academic_integrity_violation_plagiarism_facilitation
- INV_EDU_unknown_request_type_fail_closed
- INV_EDU_proposal_not_allowed
- INV_EDU_proposal_drift_requires_recommit:<keys>
- INV_EDU_malformed_input
- INV_EDU_malformed_proposal:<key>
- INV_EDU_malformed_timestamps
- INV_EDU_malformed_request_fields
