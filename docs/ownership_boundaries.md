# Ownership Boundaries (Month 14.3)

This document defines **what VERA owns and what it explicitly does not own**.
It exists to prevent misuse, confusion, and authority creep in integrations.

These boundaries are non-negotiable.

---

## What VERA owns

VERA owns **governance only**.

Specifically, VERA owns:
- Proposal normalization
- Deterministic decision-making
- Refusal, failure, and unavailability semantics
- Commit validation (explicit, synchronous)
- Append-only ledger records
- Auditability of governance outcomes

VERA’s authority ends at the ledger.

---

## What VERA does not own

VERA explicitly does **not** own:

### Execution
- Running commands
- Calling APIs
- Performing side effects
- Scheduling or retrying actions

### Permissions & consent
- Granting permissions
- Requesting permissions
- Storing permissions
- Interpreting platform consent

### UI & interaction
- Rendering interfaces
- Designing flows
- Prompting users
- Confirmations beyond commit validation

### Control & enforcement
- Preventing host execution
- Policing host behavior
- Rate limiting
- Alerting or nudging

### Intelligence & optimization
- Predicting user intent
- Optimizing success rates
- Coaching behavior
- Learning from outcomes

---

## Boundary enforcement model

VERA enforces boundaries by:
- Refusing when requests exceed scope
- Failing when safe evaluation is impossible
- Recording misuse patterns in the ledger

VERA does **not** enforce boundaries by:
- Blocking host execution
- Revoking access
- Escalating privileges
- Issuing warnings or punishments

Misuse is observable, not corrected.

---

## Common misuse patterns (anti-patterns)

The following invalidate the integration:

- Executing on ALLOW_FOR_COMMIT without an explicit commit
- Reusing a prior commit for a new proposal
- Treating ledger access as a control signal
- Hiding refusals or failures to “improve UX”
- Adding background execution tied to VERA outcomes
- Inferring permission from prior success

---

## Responsibility clarity

If something happens:
- Without a commit → the host is responsible
- With a commit → the user exercised authority
- After a refusal or failure → execution is a host violation
- Outside VERA → VERA is not accountable

This clarity is intentional.

---

## Removal test

A correct integration must pass this test:

> If VERA is removed entirely, the host system still functions,
> with fewer guardrails but no broken execution paths.

If removal breaks execution, the integration is invalid.

---

## Final boundary rule

If a feature requires VERA to own anything listed above,
that feature is forbidden.

---

Status: Month 14 — Ownership Boundaries  
Change policy: clarification-only changes allowed; no power expansion without invariant revision  
Review expectation: written to survive adversarial review
