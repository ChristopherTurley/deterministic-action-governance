# Allowed Expansions (Month 15.1)

This document defines expansions that are allowed **only if** they do not violate:
- `docs/invariants.md`
- `docs/vera_will_never.md`
- refusal/failure semantics
- proposal → decision → commit separation

Allowed expansions increase **clarity, auditability, and integrator correctness**.
They must not increase system power.

---

## Expansion rule (gate)

An expansion is allowed only if all are true:
- No new execution path is introduced
- No background behavior is introduced
- No implicit authority is introduced
- No permission/consent brokering is introduced
- Removing the expansion does not change decision outcomes
- The expansion is observable-only or contract-clarifying

If any condition is false, the expansion is forbidden.

---

## Allowed expansions (whitelist)

### 1) More refusal reason codes (clarification-only)
Add new reason codes when:
- they reduce ambiguity
- they do not change decision boundaries
- they are mapped deterministically

Examples:
- finer-grained scope codes
- clearer invariant codes

---

### 2) More failure narratives and failure types (clarification-only)
Add failure narratives to:
- improve operator understanding
- improve audit clarity

Must not introduce:
- retries
- auto-recovery
- background checks

---

### 3) Ledger schema clarity improvements (no control)
Allowed:
- adding fields that improve auditability (e.g., correlation IDs, hashes)
- adding explicit timestamps
- adding immutable references

Not allowed:
- fields that become control signals (e.g., “retry_now”, “escalate”)

---

### 4) Deterministic explanation artifacts (read-only)
Allowed:
- post-hoc summaries derived from ledger history
- timeline clarifiers
- drift summaries

Not allowed:
- recommendations
- coaching
- nudges
- alerts that prompt behavior

---

### 5) Integration contract refinement (compatibility-preserving)
Allowed:
- clearer definitions
- additional examples
- compatibility notes
- explicit anti-patterns

Not allowed:
- host enforcement requirements
- new mandatory dependencies
- platform lock-in

---

### 6) Test harness expansion (skeptic-proofing)
Allowed:
- more adversarial vectors
- regression tests for invariants
- negative tests for autonomy drift
- contract validation tests

Not allowed:
- tests that implicitly approve unsafe behavior “for convenience”

---

### 7) Multi-hat coexistence clarity (routing semantics only)
Allowed:
- making hat selection more explicit and auditable
- clearer refusal reasons when hat selection is ambiguous

Not allowed:
- implicit auto-selection that increases authority
- background hat switching

---

### 8) Documentation hardening (external intelligibility)
Allowed:
- clearer repo navigation
- shorter “scan docs”
- explicit “what never happens” expansions
- neutral platform mappings

Not allowed:
- marketing claims
- promises of outcomes
- “agent-like” framing

---

## Allowed “power-neutral” integrations

Integrations are allowed if they:
- submit proposals
- receive decisions
- request explicit commits
- read ledgers for audit

Integrations are not allowed if they:
- execute without commit
- reuse commits
- treat ledger as control
- add background automation based on VERA outputs

---

## Removal test (non-negotiable)

Every allowed expansion must pass:

> Removing it does not change core decision outcomes,
> only the clarity of explanation or audit.

If removal changes behavior, it is not allowed under this document.

---

Status: Month 15 — Allowed Expansions
Change policy: clarification-only changes allowed; no power expansion without invariant revision
Review expectation: written to survive adversarial review
