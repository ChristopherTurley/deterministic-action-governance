# Appendix: Governance Cannot Be Bolted On Later (Public, Pared-Down)

Scope: why PROPOSE/COMMIT, default-deny, nonce single-shot, and receipts must exist *before* capability expands.
Tone: non-accusatory; platform-primitive framing.

## Thesis
Once a system can cause side effects, any missing governance primitive becomes a permanent tax:
- harder to retrofit
- harder to audit
- harder to revoke
- harder to explain to users, enterprises, and regulators

So the right order is:
**governance envelope first → capability second**.

---

## Why it’s hard to retrofit (5 reasons)

### 1) Authority smears into “helpfulness”
If there is no first-class boundary between proposal and commit, product layers compensate with:
- “Are you sure?” prompts
- heuristics
- UI confirmations
- soft policies
Over time, these become inconsistent and bypassable because they’re not an execution primitive.

### 2) Default-allow becomes the hidden baseline
If side effects are allowed by default, later “policy controls” are forced to patch a sprawling surface area:
- per-app rules
- per-feature exceptions
- per-model behaviors
This produces governance drift: the system behaves differently across contexts with no stable guarantees.

### 3) Auditability must be end-to-end, not optional
Logs that are “best effort” are not receipts.
A receipt chain is a standardized artifact that can be:
- generated deterministically
- verified independently
- correlated to a specific commit nonce
Without it, trust becomes a claim instead of a verifiable property.

### 4) Replay / retry behavior becomes ambiguous
As capability expands, systems add retries, queues, and backoff.
If single-shot nonce enforcement is not foundational, you inherit “did it run twice?” ambiguity and cannot prove the negative.

### 5) Explanations become accidental policy
If the explanation layer can influence decisions—even subtly—then the system’s authority is no longer legible.
Separating:
- the decision artifact (authoritative)
- the explanation (replaceable, non-decisional)
must be structural, not conventional.

---

## Minimal takeaway
The missing primitives are governance primitives, not model features:

- PROPOSE vs COMMIT (operator confirmation primitive)
- default-deny side effects (policy envelope)
- single-shot nonce (replay protection)
- tamper-evident receipts (audit artifact)
- explanation non-interference (coats)

VERA exists to demonstrate these as testable guarantees in a reference artifact.
