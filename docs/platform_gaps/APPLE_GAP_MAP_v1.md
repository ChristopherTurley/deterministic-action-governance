# Apple Platform Gap Map (v1): Deterministic Execution Boundary Primitive

Status: Public reference note (non-prescriptive)  
Audience: platform / security / integrity / developer frameworks  
Repo posture: governance-first reference artifact; no autonomy; no background behavior

This document maps an *execution-governance primitive* to common platform surfaces, without proposing specific APIs.

---

## 1) The gap in one sentence

Modern AI-to-tool stacks can decide safely, but lack a first-class, test-enforced, revocable boundary that guarantees **explicit operator commit + single-shot side effect + receipts** before any irreversible action.

---

## 2) Definitions (tight)

- **Decision**: intent resolution, routing, recommendation, plan selection.
- **Execution**: any irreversible side effect (data mutation, network call, device state change).

A **deterministic execution boundary** is a platform-enforced separation where:
- decisions may occur freely
- execution requires an explicit operator commit artifact
- execution is at-most-once (replay/dup blocked)
- execution is allow-listed (no implicit handlers)
- revocation disables immediately
- receipts are tamper-evident and audit-legible
- inaction is a correct terminal outcome

---

## 3) Where this shows up on Apple platforms (surface-level mapping)

This is a conceptual mapping, not a critique.

### A) Intent / tool invocation surfaces (e.g., App Intents–style flows)
Observed challenge:
- handler execution often becomes the place where “decision” and “side effect” mix

Boundary requirement:
- split the lifecycle into explicit artifacts:
  - Decision (PROPOSE) → Commit (operator) → Execute (single-shot) → Receipt chain

Desired property:
- a developer can prove in tests that:
  - no execution occurs without commit
  - execution cannot be replayed
  - revocation works instantly

### B) Permission / consent prompts
Observed challenge:
- “permission granted” can be confused with “execution authorized now”

Boundary requirement:
- permission is necessary but not sufficient
- execution authorization is a distinct, explicit operator commit step
- commit is narrow, contextual, and single-shot

### C) Background / scheduling primitives
Observed challenge:
- background work can quietly convert “intent” into “follow-through”

Boundary requirement:
- no background execution by default
- any delayed work must preserve the same commit + single-shot + receipt constraints

### D) Audit / provenance
Observed challenge:
- logs exist, but are often not normative artifacts

Boundary requirement:
- receipts are part of the execution lifecycle
- receipts are tamper-evident (checksummed)
- receipts include:
  - what was proposed
  - what was committed
  - what executor ran
  - what was revoked/blocked
  - what result was produced

---

## 4) What this repo provides (evidence, not promises)

This repo demonstrates the boundary as mechanics:
- strict artifacts for decision + commit
- replay guard (nonce)
- executor allow-list + enable/disable (revocation)
- receipt chain integrity (tamper-evident)
- explicit “no background behavior” constraints
- test-enforced invariants

No external calls are required to evaluate these claims.

---

## 5) How to evaluate (one command)

python3 -m pytest

If the tests pass, the boundary properties above are intended to be enforced rather than described.

---

## 6) Non-goals

- Not requesting a new Apple API
- Not proposing an agent framework
- Not asserting current systems are unsafe
- Not providing a product

This is a reference map to a missing primitive that becomes important as AI systems gain richer tool access.
