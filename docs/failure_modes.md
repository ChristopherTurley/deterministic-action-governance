# Failure Modes (Narratives v1)

## Definition of failure (VERA terms)
A failure is a breakdown in expected operation.
It is **not** a policy decision and **not** a refusal.

Failures must:
- Fail closed
- Surface clearly
- Produce no automatic recovery actions
- Preserve auditability

Failures never justify execution.

---

## Failure vs refusal (quick reminder)

- **Refusal**: deliberate, correct “no” based on authority, scope, safety, invariants, or context TTL
- **Failure**: the system could not proceed as designed

Rule:
If the system *cannot safely decide*, it fails.
If the system *decides no*, it refuses.

---

## Failure narratives

Each narrative is intentionally simple and repeatable.

---

### 1) Schema Validation Failure

**Trigger**
Incoming proposal payload does not conform to the expected schema.

**User sees**
“Something went wrong while validating this request. No action was taken.”

**Ledger records**
- decision: FAILURE
- failure_type: SCHEMA_VALIDATION
- action_taken: none
- recoverable: yes

**System does next**
Nothing automatically. User must re-submit a valid request.

---

### 2) Missing Required Configuration

**Trigger**
An optional integration is referenced but not configured.

**User sees**
“This capability isn’t configured. No action was taken.”

**Ledger records**
- decision: FAILURE
- failure_type: MISSING_CONFIGURATION
- integration: <name>
- action_taken: none

**System does next**
Nothing. Configuration must be completed explicitly.

---

### 3) External Dependency Unavailable

**Trigger**
Required external service is unreachable (network, API down).

**User sees**
“This service is currently unavailable. No action was taken.”

**Ledger records**
- decision: FAILURE
- failure_type: DEPENDENCY_UNAVAILABLE
- dependency: <name>
- action_taken: none

**System does next**
Nothing. No retries, no background polling.

---

### 4) Ledger Write Failure

**Trigger**
The system cannot persist the decision record safely.

**User sees**
“A system error occurred while recording this action. No action was taken.”

**Ledger records**
- decision: FAILURE
- failure_type: LEDGER_WRITE_FAILURE
- action_taken: none

**System does next**
Nothing. Execution is blocked because auditability is required.

---

### 5) Internal Exception (Caught)

**Trigger**
An unexpected but handled exception occurs during processing.

**User sees**
“An internal error occurred. No action was taken.”

**Ledger records**
- decision: FAILURE
- failure_type: INTERNAL_EXCEPTION
- exception_id: <opaque id>
- action_taken: none

**System does next**
Nothing. No fallback behavior is allowed.

---

### 6) Context Serialization Failure

**Trigger**
Context cannot be safely serialized or restored.

**User sees**
“Context could not be processed safely. No action was taken.”

**Ledger records**
- decision: FAILURE
- failure_type: CONTEXT_SERIALIZATION
- action_taken: none

**System does next**
Nothing. User must restate context.

---

### 7) Determinism Guard Triggered

**Trigger**
System detects non-deterministic routing or ambiguous internal state.

**User sees**
“The system could not proceed deterministically. No action was taken.”

**Ledger records**
- decision: FAILURE
- failure_type: DETERMINISM_GUARD
- action_taken: none

**System does next**
Nothing. Ambiguity halts processing.

---

### 8) Timeout During Evaluation

**Trigger**
Evaluation exceeds allowed time budget.

**User sees**
“The request timed out before a safe decision could be made. No action was taken.”

**Ledger records**
- decision: FAILURE
- failure_type: EVALUATION_TIMEOUT
- action_taken: none

**System does next**
Nothing. User may retry explicitly.

---

### 9) Corrupted Prior State Detected

**Trigger**
Previously stored state fails integrity checks.

**User sees**
“A prior state issue was detected. No action was taken.”

**Ledger records**
- decision: FAILURE
- failure_type: STATE_CORRUPTION
- action_taken: none

**System does next**
Nothing. Manual recovery required.

---

### 10) Unsupported Runtime Environment

**Trigger**
Runtime conditions do not meet required guarantees.

**User sees**
“This environment is not supported for safe operation. No action was taken.”

**Ledger records**
- decision: FAILURE
- failure_type: UNSUPPORTED_ENVIRONMENT
- action_taken: none

**System does next**
Nothing. Environment must be corrected.

---

## Global failure rules

On any failure:
- No execution occurs
- No retries occur
- No permissions are requested
- No authority is inferred
- No automatic recovery is attempted

Failures preserve safety by doing nothing.

---

Status: Month 11 — Failure Narratives v1
Change policy: clarification-only changes allowed; no power expansion without invariant revision
Review expectation: written to survive adversarial review
