# High-Focus Worker Hat v1 — Governance Specification

Status: Draft v1
Scope: Governance-only
Power: Zero

## Purpose
Preserve explicit focus constraints and explain drift post-hoc without nudging.

Never:
- time tracking
- productivity scoring
- nudging or coaching

## Domain Declaration (Vocabulary Only)
- DECLARE_FOCUS_CONSTRAINTS
- PROPOSE_TASK
- PROPOSE_CONTEXT_SWITCH
- RECORD_DECISION

## Invariants (Refusal-Only)
category=INVARIANT. Reason codes:
- INV_FOCUS_NO_NUDGING
- INV_FOCUS_CONSTRAINT_VIOLATION
- INV_FOCUS_MISSING_CONTEXT
