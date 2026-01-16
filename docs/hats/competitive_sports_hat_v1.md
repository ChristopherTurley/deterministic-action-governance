**Document Type:** Reference Library  
**Required for Evaluation:** No  
**Primary Evaluator Path:** `docs/START_HERE.md`

# Competitive Sports Hat v1 — Governance Specification

Status: Draft v1
Scope: Governance-only
Power: Zero

## Purpose
Preserve authority and accountability for time-sensitive competitive decisions.
This is journaling + governance, not strategy optimization.

Never:
- strategy recommendations
- performance optimization
- automation

## Domain Declaration (Vocabulary Only)
Shared:
- RECORD_DECISION
- CHALLENGE_CALL
- SUBSTITUTION_CALL
- DECLARE_TEAM_BOUNDARIES

Sport vocabularies may be appended as names only (no logic).

## Invariants (Refusal-Only)
category=INVARIANT. Reason codes:
- INV_SPORTS_NO_OPTIMIZATION
- INV_SPORTS_AUTHORITY_REQUIRED
- INV_SPORTS_MISSING_CONTEXT
