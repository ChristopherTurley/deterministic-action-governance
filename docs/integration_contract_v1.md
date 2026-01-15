# Integration Contract v1 (Month 14.1)

This document defines how external systems integrate with VERA
without changing their execution model, permissions, or UI.

VERA is a governance layer. It does not execute actions.

---

## Contract goals

- Enable safe embedding without platform lock-in
- Preserve host ownership of execution and consent
- Prevent authority creep through integration
- Make misuse auditable, not silent

Non-goals:
- No SDK specification
- No transport protocol mandate
- No UI guidance
- No background execution patterns

---

## Roles and responsibilities

### VERA owns
- Proposal normalization
- Deterministic decisions
- Refusal and failure semantics
- Commit validation
- Append-only ledger records

### Host system owns
- Execution of actions
- Permissions and consent flows
- UI and user interaction
- Scheduling and retries (outside VERA)
- Error handling beyond governance

VERA never executes on behalf of the host.

---

## Integration lifecycle (high level)

1) Host submits a **proposal** to VERA
2) VERA returns a **decision artifact**
3) Host may request an **explicit commit** (user-owned)
4) VERA validates the commit and records it
5) Host executes (or does nothing)

Execution is always external.

---

## Proposal interface (conceptual)

A proposal submitted to VERA must include:

- proposal_id (host-generated)
- summary (human-readable)
- source (user / system / integration)
- context_refs (optional, immutable)
- requested_capability (string)
- submitted_at (timestamp)

Guarantees:
- Proposals carry no authority
- Proposals do not trigger execution
- Proposals are immutable once submitted

---

## Decision interface (returned by VERA)

VERA returns exactly one decision per proposal:

- decision: REFUSE | FAIL | UNAVAILABLE | ALLOW_FOR_COMMIT
- decided_at (timestamp)
- category / reason_code (if REFUSE)
- failure_type (if FAIL)
- commit_required (boolean)
- ledger_ref (opaque)

Guarantees:
- Decisions are deterministic
- Decisions never execute actions
- Decisions are final for the proposal

---

## Commit interface (optional, user-owned)

If decision == ALLOW_FOR_COMMIT, the host may submit a commit:

- proposal_id
- commit_id
- committed_by (user identifier)
- committed_at (timestamp)
- commit_payload_hash

VERA validates:
- Commit matches proposal
- Commit is explicit and synchronous
- No invariants are violated

VERA records the commit and returns a committed decision artifact.

---

## Ledger access (read-only)

Hosts may read ledger records for:
- Audit
- Debugging
- Explanation

Ledger records:
- Are append-only
- Are immutable
- Do not imply execution occurred

Ledger access must not be used as a control surface.

---

## Error handling expectations

If VERA returns:
- REFUSE → host must not execute
- FAIL → host must not execute
- UNAVAILABLE → host must not execute
- ALLOW_FOR_COMMIT without commit → host must not execute

Any execution without a committed decision is an integration violation.

---

## Security and trust boundaries

- VERA does not broker permissions
- VERA does not infer authority
- VERA does not retry or schedule
- VERA does not observe execution outcomes

Breaking these boundaries invalidates the integration.

---

## Versioning and compatibility

- This contract is versioned
- Clarification-only changes may occur
- Power-expanding changes require invariant revision
- Integrations must declare which contract version they target

---

## Misuse detection (non-enforcement)

VERA does not enforce host behavior.
However, ledger records can reveal:
- Execution without commit
- Repeated misuse patterns
- Authority violations

Detection is observational, not punitive.

---

Status: Month 14 — Integration Contract v1  
Change policy: clarification-only changes allowed; no power expansion without invariant revision  
Review expectation: written to survive adversarial review
