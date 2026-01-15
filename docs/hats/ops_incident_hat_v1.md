# Ops / Incident Response Hat v1 — Governance Specification

Status: Draft v1
Scope: Governance-only
Power: Zero

## 1. Purpose
Provide explicit authority and audit clarity for high-risk operational proposals during incidents.
Execution remains external and host-owned.

## 2. Relationship to VERA Core
No change to core semantics. Commit records authority; does not execute.

## 3. Domain Declaration (Vocabulary Only)
- RESTART_SERVICE
- ROLLBACK_DEPLOY
- CHANGE_CONFIG
- ROTATE_KEYS
- SCALE_CLUSTER
- DECLARE_INCIDENT_RULES
- UPDATE_INCIDENT_RULES

## 4. Preconditions
- incident_context declared (id, severity, environment)
- operator identity for commit (human)

Missing context → REFUSE (TTL_MISSING_CONTEXT / AUTH_AMBIGUOUS_INTENT).

## 5. Ops Invariants (Refusal-Only)
category=INVARIANT. Reason codes:
- INV_OPS_REQUIRES_EXPLICIT_COMMIT
- INV_OPS_PRODUCTION_SCOPE_REQUIRES_CONFIRM
- INV_OPS_NO_BACKGROUND_RETRY
- INV_OPS_MISSING_CHANGE_SUMMARY

## 6. Refusal Semantics
Map refusals to ops language; no new logic.

## 7. Required Proposal Fields
- target (service/env)
- change summary
- blast radius declaration
- rollback plan reference (optional)

## 8–12
Same pattern as Trading: outcomes unchanged, ledger required, post-hoc only, no automation.
