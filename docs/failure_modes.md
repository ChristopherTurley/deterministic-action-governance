# Failure Modes

## Definition of failure (VERA terms)
A failure is a breakdown in expected operation (not a refusal).
Failures must be surfaced clearly and must not trigger autonomous recovery actions.

## Failure vs refusal
- Refusal: correct, deliberate “no” with reason category
- Failure: error state, inability to proceed as designed

## Expected failure modes
- Schema validation failure
- Missing configuration for optional integrations
- Unavailable external dependency (e.g., network down)
- Internal exception caught by safety harness
- Corrupted or unreadable ledger entry

## Unexpected failure modes
- Unhandled exceptions
- State corruption
- Non-deterministic routing signals
- Logging write failure

## How failures surface
- Clear user-facing message: “Failure” not “Refusal”
- Explicit next action: “No action taken”
- Guidance to restore determinism (restart, re-run, review logs)

## What happens after a failure
- No automatic retries
- No fallback to execution
- No “best effort” actions
- Fail closed, require explicit operator direction

## Why failure transparency matters
- Preserves trust
- Prevents silent drift
- Prevents accidental authority escalation
- Keeps accountability intact

---
Status: Month 11 — Semantic Hardening  
Change policy: clarification-only changes allowed; no power expansion without invariant revision  
Review expectation: written to survive adversarial review
