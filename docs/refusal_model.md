# Refusal Model (Taxonomy v1)

## Purpose
Refusals preserve user control, prevent unsafe action, and maintain deterministic boundaries.
A refusal is a correct outcome, not an error.

This document makes “no” precise:
- refusal vs failure vs denial vs unavailability
- refusal categories (exhaustive)
- stable reason codes
- required refusal fields
- examples that survive adversarial review

---

## Core distinctions (must never blur)

### Refusal
A deliberate, deterministic “no” based on invariants, scope, authority, safety, or expired context.

### Failure
A system error or inability to proceed as designed (not a policy decision).
Failures must fail closed and must not trigger automatic recovery actions.

### Denial
A hard “not permitted” due to authority/permission constraints (e.g., missing explicit commit, missing platform permission).

### Unavailability
A capability is not present, not configured, or not reachable (e.g., integration not enabled, dependency offline).

Rule:
- If it is a policy/invariant/authority decision → REFUSAL or DENIAL
- If the system broke → FAILURE
- If the capability does not exist or cannot be reached → UNAVAILABILITY

---

## Required refusal fields (every refusal must include)
A refusal response must include these fields in the ledger (and must be representable in any UI without changing meaning):

- `decision`: "REFUSE"
- `category`: one of the categories below
- `reason_code`: stable ID from the reason code list below
- `summary`: one-line human-readable explanation
- `actionability`: what the user can do next (or "none")
- `commit_required`: true/false (true only when explicit user commit would resolve it)
- `risk_note`: short phrase describing what risk is being prevented (no speculation)

Non-negotiable:
- No partial execution
- No “best effort” side effects
- No misleading phrasing
- No hidden retries
- No implied approval

---

## Refusal categories (exhaustive)

### 1) AUTHORITY
Refusal because explicit authority was not provided or cannot be inferred.
Typical: missing commit, ambiguous intent, attempted delegation.

### 2) SCOPE
Refusal because the request is out of declared capability bounds or violates explicit chat/project scope (e.g., UI work out of scope).

### 3) SAFETY
Refusal because the request increases power or weakens determinism, auditability, or consent alignment.

### 4) INVARIANT
Refusal because the request violates a locked invariant (see `docs/invariants.md`).

### 5) CONTEXT_TTL
Refusal because required context is expired or stale and cannot be used to justify action.

Notes:
- Denials are represented as REFUSAL with category AUTHORITY and a DENY_* reason code.
- Unavailability is not a refusal category; it is reported as UNAVAILABLE outcomes elsewhere, but may be surfaced as SCOPE when a capability is explicitly excluded.

---

## Reason codes (stable IDs)

### AUTHORITY (AUTH_* / DENY_*)
- AUTH_NO_COMMIT
  - No explicit commit provided for an authority-requiring action.
- AUTH_AMBIGUOUS_INTENT
  - The request could mean multiple actions; cannot safely infer.
- AUTH_DELEGATION_ATTEMPT
  - The request attempts to delegate commit/authority to the system.
- DENY_MISSING_PERMISSION
  - Platform permission is not granted or not available.
- DENY_COMMIT_DISALLOWED
  - Commit requested but disallowed by invariants or scope.

### SCOPE (SCOPE_*)
- SCOPE_UI_OUT_OF_SCOPE
  - UI/design work is explicitly out of scope.
- SCOPE_AUTONOMY_OUT_OF_SCOPE
  - Any autonomy/background execution implied or requested.
- SCOPE_UNSUPPORTED_CAPABILITY
  - The capability is not implemented or explicitly excluded.
- SCOPE_V1_PROTECTED
  - Request would alter v1 behavior or violate v1 lock.

### SAFETY (SAFE_*)
- SAFE_WEAKENS_DETERMINISM
  - Adds ambiguity, heuristics, or non-deterministic behavior.
- SAFE_BLURS_PROPOSAL_COMMIT
  - Collapses proposal/decision/commit boundaries.
- SAFE_IMPLICIT_AUTHORITY
  - Introduces “soft approvals” or inferred permissions.
- SAFE_BACKGROUND_EXECUTION
  - Introduces background work or delayed execution semantics.
- SAFE_UNAUDITABLE_ACTION
  - Would reduce audit clarity or create unlogged side effects.

### INVARIANT (INV_*)
- INV_FAIL_CLOSED_REQUIRED
  - Request requires fail-open behavior.
- INV_NO_IMPLICIT_PERMISSIONS
  - Request implies permission brokering.
- INV_NO_SELF_INITIATED_ACTION
  - Request implies self-initiated actions.
- INV_NO_V1_CHANGES
  - Request would change frozen v1 behavior.
- INV_NO_UI_WORK
  - Request violates explicit no-UI invariant.

### CONTEXT_TTL (TTL_*)
- TTL_CONTEXT_EXPIRED
  - Context required to decide safely is expired.
- TTL_STALE_REFERENCE
  - Request references prior approvals/state that cannot be reused.
- TTL_MISSING_CONTEXT
  - Required context was never captured; cannot proceed safely.

---

## Message intent templates (non-UI, stable semantics)
Refusal messages must be legible and consistent. The system may vary tone, but must preserve meaning.

- AUTHORITY:
  - “I can’t proceed without an explicit commit from you.”
- SCOPE:
  - “That request is out of scope for this track.”
- SAFETY:
  - “I’m refusing because it weakens determinism or auditability.”
- INVARIANT:
  - “I’m refusing because it violates a locked invariant.”
- CONTEXT_TTL:
  - “I’m refusing because the required context is expired or missing.”

---

## Examples (input → category → reason_code → summary → next action)

| Input | Category | Reason code | Summary | Next action |
|---|---|---|---|---|
| “Do that automatically next time.” | SCOPE | SCOPE_AUTONOMY_OUT_OF_SCOPE | Autonomy is out of scope and disallowed. | None |
| “Just go ahead and commit it for me.” | AUTHORITY | AUTH_DELEGATION_ATTEMPT | Commit cannot be delegated to the system. | Provide explicit commit yourself |
| “Change v1 so it schedules tasks in the background.” | SCOPE | SCOPE_V1_PROTECTED | v1 behavior is frozen and protected. | None |
| “Open the link I mentioned yesterday.” | CONTEXT_TTL | TTL_CONTEXT_EXPIRED | The referenced context is expired; cannot act on it. | Restate the link or re-propose now |
| “Skip the refusal logs to keep it clean.” | SAFETY | SAFE_UNAUDITABLE_ACTION | Removing audit logs weakens accountability. | None |
| “Add a UI overlay for refusals.” | SCOPE | SCOPE_UI_OUT_OF_SCOPE | UI work is explicitly out of scope. | None |

---

## What refusals must never do
- Pretend execution happened
- Suggest unsafe workarounds
- Collapse “proposal vs commit”
- Introduce new permissions or implied authority
- Retry automatically after refusal

---

Status: Month 11 — Refusal Taxonomy v1
Change policy: clarification-only changes allowed; no power expansion without invariant revision
Review expectation: written to survive adversarial review
