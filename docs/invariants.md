# Invariants

## Definition (VERA terms)
An invariant is a non-negotiable rule that limits system power and preserves determinism.
If any invariant is broken, VERA is no longer VERA.

## Global invariants (never negotiable)
- Fail closed by default
- Prefer refusal over unsafe action
- Surface drift explicitly
- Produce auditable ledgers
- No hidden state mutations

## Authority invariants
- No implicit authority
- No inferred permissions
- No “soft approvals”
- No chained commits
- No delegated commit without explicit, synchronous user intent

## Execution invariants
- No background execution
- No self-initiated action
- No action without explicit user commit
- No silent retries
- No side effects on proposal generation

## Permission invariants
- VERA does not grant, request, store, proxy, or reinterpret permissions
- Platform consent remains the source of truth
- VERA remains downstream of consent

## Temporal invariants
- No delayed authority
- No scheduled commits
- Context has explicit TTL; expired context cannot be used to justify action

## Drift prevention rules
- Any change that increases power requires:
  - explicit invariant review
  - explicit doc updates
  - explicit test updates
- Ambiguity is treated as a refusal condition

## Invalidation conditions
If any of the following occur, the artifact is invalid:
- Background execution is introduced
- Implicit permissions are introduced
- Proposal and commit boundaries are blurred
- V1 behavior is changed
- Unsafe convenience overrides determinism

---
Status: Month 11 — Semantic Hardening
Change policy: clarification-only changes allowed; no power expansion without invariant revision
Review expectation: written to survive adversarial review
