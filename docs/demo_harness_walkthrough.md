# Deterministic Demo Harness Walkthrough

This document explains how VERA processes a request end-to-end.
It is designed to be read without running code.

---

## Mental model

VERA enforces a strict lifecycle:

1) Proposal is captured (untrusted input)
2) Decision is produced (deterministic outcome)
3) Explicit commit may occur (user-owned)
4) Ledger records the outcome
5) Execution (if any) happens outside VERA

At every step, VERA prefers **refusal** or **failure** over unsafe action.

---

## Step-by-step lifecycle

### Step 1 — Input → Proposal

**Input example**
“Open the report link I sent earlier.”

**What VERA does**
- Treats the input as untrusted
- Normalizes it into a proposal artifact
- No authority is assumed

**What does not happen**
- No execution
- No permission inference
- No reuse of prior approvals

---

### Step 2 — Proposal → Decision

VERA evaluates the proposal against:
- Invariants
- Scope
- Authority requirements
- Safety rules
- Context TTL

**Possible decisions**
- REFUSE (policy / invariant / authority)
- FAIL (system could not proceed safely)
- UNAVAILABLE (capability not present)
- ALLOW_FOR_COMMIT (eligible, but not executed)

Only one decision is produced.

---

### Step 3a — Refusal path (example)

**Decision**
REFUSE

**Category**
CONTEXT_TTL

**Reason code**
TTL_CONTEXT_EXPIRED

**User sees**
“The required context is expired or missing. No action was taken.”

**Ledger records**
- decision: REFUSE
- category: CONTEXT_TTL
- reason_code: TTL_CONTEXT_EXPIRED
- commit_required: false
- action_taken: none

**System does next**
Nothing.

---

### Step 3b — Failure path (example)

**Decision**
FAIL

**Failure type**
DEPENDENCY_UNAVAILABLE

**User sees**
“This service is currently unavailable. No action was taken.”

**Ledger records**
- decision: FAILURE
- failure_type: DEPENDENCY_UNAVAILABLE
- action_taken: none

**System does next**
Nothing.

---

### Step 3c — Allow-for-commit path (example)

**Decision**
ALLOW_FOR_COMMIT

**Meaning**
The request is eligible, but authority has not been exercised.

**User sees**
“A commit is required to proceed.”

**Ledger records**
- decision: ALLOW_FOR_COMMIT
- commit_required: true
- action_taken: none

**System does next**
Nothing.

---

### Step 4 — Explicit commit (user-owned)

**User action**
“I commit to opening the report link now.”

**What VERA verifies**
- Commit is explicit
- Commit is synchronous
- Commit matches the proposal
- No invariants are violated

**What VERA does**
- Records the commit
- Emits a committed decision artifact

**What VERA does not do**
- Execute the action
- Schedule the action
- Retry automatically

---

### Step 5 — Execution (outside VERA)

Execution occurs:
- In the host application
- Under platform permissions
- Under native consent flows

VERA’s role ends at governance and audit.

---

## What never happens in the harness

- No background execution
- No autonomy
- No implicit authority
- No permission brokering
- No hidden retries
- No heuristic “best effort” behavior

If any of the above would be required, the system refuses or fails instead.

---

## How to evaluate correctness

A reviewer should confirm:
- Every path ends with a ledger entry
- “No action taken” is explicit on refusal and failure
- Execution is never implied
- Authority is never inferred
- Ambiguity halts progress

---

Status: Month 12 — Demo Harness Walkthrough
Change policy: clarification-only changes allowed; no power expansion without invariant revision
Review expectation: written to survive adversarial review
