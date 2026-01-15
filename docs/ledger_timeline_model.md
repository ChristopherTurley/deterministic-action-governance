# Ledger Timeline Model (Month 13.1)

This document defines how VERA represents time, causality, and accountability
across proposal, decision, commit, and outcome — without adding control.

The goal is **clarity**, not action.

---

## Design goals

- Make timelines legible to humans and machines
- Preserve determinism and auditability
- Avoid introducing any execution or control surface
- Enable after-the-fact understanding without nudging behavior

Non-goal:
- No UI requirements
- No dashboards
- No alerts
- No automation

---

## Core timeline entities

### 1) Proposal Event
Represents untrusted input normalized into a proposal artifact.

Required fields:
- event_type: PROPOSAL
- proposal_id
- captured_at (timestamp)
- source (user / system / integration)
- summary (human-readable)
- context_refs (optional)

Guarantees:
- No authority
- No execution
- Immutable once recorded

---

### 2) Decision Event
Represents the system’s deterministic evaluation of a proposal.

Required fields:
- event_type: DECISION
- proposal_id
- decision (REFUSE / FAIL / UNAVAILABLE / ALLOW_FOR_COMMIT)
- decided_at (timestamp)
- category (if REFUSE)
- reason_code (if REFUSE)
- failure_type (if FAIL)
- commit_required (true/false)

Guarantees:
- Exactly one decision per proposal
- Decision does not execute anything
- Decision is final unless a new proposal is made

---

### 3) Commit Event
Represents explicit, synchronous user authority.

Required fields:
- event_type: COMMIT
- proposal_id
- commit_id
- committed_at (timestamp)
- committed_by (user)
- commit_payload_hash

Guarantees:
- Only possible if decision == ALLOW_FOR_COMMIT
- Cannot occur automatically
- Cannot be inferred or reused

---

### 4) Outcome Event
Represents the terminal result from VERA’s perspective.

Required fields:
- event_type: OUTCOME
- proposal_id
- outcome (NO_ACTION / COMMITTED)
- recorded_at (timestamp)

Notes:
- NO_ACTION covers refusals and failures
- COMMITTED indicates authority was exercised, not that execution occurred

---

## Timeline invariants

- Events are append-only
- Events are strictly ordered per proposal
- No event mutates a prior event
- Missing events are meaningful (e.g., no COMMIT means no authority)

Breaking any invariant invalidates the ledger.

---

## Example timelines

### Example A — Refusal (context expired)

1. PROPOSAL → captured_at T1
2. DECISION (REFUSE, TTL_CONTEXT_EXPIRED) → decided_at T2
3. OUTCOME (NO_ACTION) → recorded_at T3

There is no COMMIT event.

---

### Example B — Failure (dependency unavailable)

1. PROPOSAL → T1
2. DECISION (FAIL, DEPENDENCY_UNAVAILABLE) → T2
3. OUTCOME (NO_ACTION) → T3

There is no COMMIT event.

---

### Example C — Commit path (eligible request)

1. PROPOSAL → T1
2. DECISION (ALLOW_FOR_COMMIT) → T2
3. COMMIT (explicit user action) → T3
4. OUTCOME (COMMITTED) → T4

Execution, if any, occurs outside VERA.

---

## What the timeline makes explicit

A reviewer can always answer:
- What was proposed?
- What decision was made?
- Why was it made?
- Was authority exercised?
- When did each step occur?
- What *did not* happen?

---

## What the timeline never implies

- That execution occurred
- That permission was granted
- That authority was inferred
- That retries or background actions happened

The ledger records **governance**, not behavior.

---

Status: Month 13 — Ledger Timeline Clarity  
Change policy: clarification-only changes allowed; no power expansion without invariant revision  
Review expectation: written to survive adversarial review
