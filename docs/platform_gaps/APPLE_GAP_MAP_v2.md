# Apple Platform Gap Map v2 (Public, Pared-Down)

Status: PUBLIC (non-accusatory, evaluator-safe)
Scope: Platform gap mapping + what VERA proves
Non-Goals: No execution guidance. No “agent” roadmap. No Apple criticism.

## One sentence
VERA demonstrates a deterministic governance envelope that separates "model output" from "authority to cause side effects"—and makes that separation auditable, revocable, and testable.

---

## What VERA proves (5 invariants)

### INV-1: Proposal is not authority
A model can propose an intent, but it never becomes an action without an explicit operator commit.

### INV-2: Default-deny side effects
If an effect is not allow-listed and gated, the correct outcome is refusal/inaction.

### INV-3: Single-shot execution
Every effect attempt is bound to a single commit nonce; replays are rejected deterministically.

### INV-4: Receipts are mandatory and tamper-evident
Every attempt (even inert/log-only) produces a receipt chain with checksums.

### INV-5: No background behavior
There is no scheduler, daemon loop, background polling, or silent retries—by contract and by tests.

---

## The Apple gap (5 missing primitives)

### GAP-1: Commit primitive (operator intent confirmation)
Apple has good *intent routing* surfaces (e.g., App Intents), but there is no first-class primitive that says:
- "This is a PROPOSE"
- "This becomes COMMIT only with an explicit operator confirmation token"
- "This commit is scoped, single-shot, and logged"

**Why it matters:** AI features drift into “silent action” without a standardized commit gate.

### GAP-2: Default-deny side-effect policy (system-wide)
Developers can add confirmations, but there is no system-native policy envelope that defaults to deny for side effects unless explicitly allow-listed per capability + per context.

**Why it matters:** policy becomes app-by-app and inconsistent; users cannot reason about guarantees.

### GAP-3: Replay protection + single-shot side effects
There is no platform-level replay guard binding an action attempt to a unique nonce that cannot be reused.

**Why it matters:** retries, replays, and ambiguous “did it run?” moments become unavoidable in agent-like flows.

### GAP-4: Tamper-evident receipt chains
Apple has strong logging and privacy frameworks, but no standard “receipt chain” object for AI-mediated attempts:
- preconditions
- decision snapshot
- commit snapshot
- attempt record
- result record
- checksum chain

**Why it matters:** auditability is fragmented; trust depends on vendor claims.

### GAP-5: Non-interference explanations (coats)
There is no standard separation between:
- the decision artifact (authoritative)
- the explanation layer (replaceable, non-decisional)

**Why it matters:** explanations can accidentally become policy or “soft authority,” creating hidden behavior.

---

## Where Apple would integrate this (conceptual, not prescriptive)

- **Siri / Apple Intelligence**: a first-class COMMIT primitive + receipt chain standard.
- **App Intents**: an “inert proposal” mode that cannot execute and is safe to log/share.
- **OS policy layer**: default-deny side effects with allow-list bundles (capability manifests).
- **Enterprise / regulated deployments**: standardized audit outputs and revocation semantics.

---

## The minimal takeaway
The gap is not “better models.”
The gap is a missing, standardized governance envelope:
- PROPOSE vs COMMIT
- default-deny
- single-shot nonce
- tamper-evident receipts
- explanation non-interference

VERA is a reference artifact that demonstrates these primitives as testable guarantees.

────────────────────────
You are on the Evaluator Track

Next: v2/docs/demo_index.md
Return to start: docs/START_HERE.md
