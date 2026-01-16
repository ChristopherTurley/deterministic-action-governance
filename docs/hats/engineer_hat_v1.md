**Document Type:** Reference Library  
**Required for Evaluation:** No  
**Primary Evaluator Path:** `docs/START_HERE.md`

# Engineer Hat v1 — Governance Specification

Status: Draft v1
Scope: Governance-only
Power: Zero

## Purpose
Make change authority explicit and auditable for engineering decisions without enforcing execution.

Never:
- CI/CD enforcement
- auto-rollback
- blocking host execution

## Domain Declaration (Vocabulary Only)
- PROPOSE_CHANGE
- RECORD_DECISION
- REQUIRE_EXPLICIT_COMMIT
- DECLARE_CHANGE_BOUNDARIES

## Invariants (Refusal-Only)
category=INVARIANT. Reason codes:
- INV_ENG_AUTHORITY_REQUIRED
- INV_ENG_NO_ENFORCEMENT
- INV_ENG_MISSING_CONTEXT
