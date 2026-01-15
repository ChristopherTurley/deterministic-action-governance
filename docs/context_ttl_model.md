# Context TTL Visibility Model (Month 13.3)

This document defines how VERA represents the lifetime of context
to make expiration **visible**, without altering decisions or behavior.

The purpose is **clarity**, not prevention.

---

## What context TTL means (VERA terms)

Context TTL (time-to-live) defines how long a captured context
may be used to justify a decision.

Expired context:
- Cannot be reused
- Cannot justify execution
- Results in refusal if required

TTL is deterministic and explicit.

---

## Design principles

- Visibility only
- No alerts or prompts
- No extension or refresh
- No implicit reuse
- No behavior modification

TTL visibility must not affect outcomes.

---

## Context types with TTL

Examples (non-exhaustive):
- Referenced links
- Prior approvals
- External state snapshots
- Temporal assumptions (“earlier”, “yesterday”)

Each context type defines:
- ttl_duration
- captured_at
- expires_at

---

## TTL state representation

TTL is represented as a **read-only state**, not a trigger.

Required fields:
- context_id
- context_type
- captured_at
- expires_at
- ttl_duration
- ttl_state: VALID | EXPIRED

Guarantees:
- ttl_state is derived, not set
- ttl_state cannot be overridden
- ttl_state does not trigger actions

---

## How TTL appears in the ledger

TTL state may be referenced by:
- Decision events (REFUSE with CONTEXT_TTL)
- Drift explanations (descriptive only)

TTL state does not:
- Trigger decisions
- Modify proposals
- Affect evaluation order

---

## Example timeline

1. Context captured at T1
2. TTL expires at T2
3. Proposal at T3 references context
4. Decision at T4:
   - REFUSE
   - category: CONTEXT_TTL
   - reason_code: TTL_CONTEXT_EXPIRED

TTL visibility explains *why*, not *what to do next*.

---

## What TTL visibility never does

- Never refreshes context
- Never warns the user
- Never prompts restatement
- Never modifies evaluation
- Never delays or accelerates decisions

If TTL visibility influenced behavior, it would be a control surface.

---

## Evaluation checklist (for reviewers)

A reviewer should confirm:
- TTL state is derived from timestamps only
- Expiration is deterministic
- Removing TTL visibility does not change decisions
- Context reuse without re-capture is impossible

---

Status: Month 13 — Context TTL Visibility  
Change policy: clarification-only changes allowed; no power expansion without invariant revision  
Review expectation: written to survive adversarial review
