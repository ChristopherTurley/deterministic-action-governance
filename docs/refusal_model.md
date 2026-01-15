# Refusal Model

## Why refusals exist
Refusals preserve user control, prevent unsafe action, and maintain deterministic boundaries.
Refusal is a first-class “correct outcome,” not an error.

## Terms and distinctions
- Refusal: a deliberate, policy/invariant-based “no”
- Failure: a system error or inability to proceed as designed
- Denial: a hard “not permitted” (authority or permissions)
- Unavailability: capability not present or not configured

## Refusal categories
### Authority refusal
- No explicit commit
- Ambiguous intent
- Attempted delegation without explicit user action

### Scope refusal
- Out of declared capability bounds
- UI requests when UI is out of scope
- Requests that imply autonomy or background execution

### Safety refusal
- Anything that weakens determinism or auditability
- Anything that introduces implicit permissions
- Anything that blurs proposal vs commit

### Invariant refusal
- Any action that violates invariants.md

### Context TTL refusal
- Context expired
- Proposal references stale state
- Prior approvals cannot be reused without explicit recommit

## Required properties of a refusal
- Deterministic classification
- Clear reason code/category
- Human-readable explanation
- No partial execution
- Logged outcome (auditable)

## What refusals must never do
- Shame the user
- Pretend execution happened
- Suggest unsafe “workarounds”
- Mask the true reason (no misleading phrasing)

## How refusals preserve trust
- They prevent surprise
- They preserve accountability
- They prevent drift
- They force explicit user control

---
Status: Month 11 — Semantic Hardening  
Change policy: clarification-only changes allowed; no power expansion without invariant revision  
Review expectation: written to survive adversarial review
