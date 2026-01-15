# VERA — Deterministic Action Governance Engine

## One-sentence definition
VERA is a deterministic, fail-closed governance layer that separates **proposal → decision → explicit commit**, producing auditable outcomes without autonomy.

## What this is not
- Not an agent
- Not autonomous
- Not a UI product
- Not a background task runner
- Not a permissions broker
- Not a policy/ethics engine

## Core model (non-negotiable)
- Inputs are treated as **untrusted proposals**
- The system produces a **decision** (refuse / fail / unavailable / allow-for-commit)
- **No execution occurs** without an explicit, synchronous user **commit**
- Ambiguity is resolved by **refusal** (fail closed)

## Trust anchors (start here)
- Invariants (constitution): `docs/invariants.md`
- Refusal taxonomy (reason codes + required fields): `docs/refusal_model.md`
- Failure narratives (what happens when things break): `docs/failure_modes.md`
- Explicit non-goals (fast scan): `docs/vera_will_never.md`
- Security review simulation (hostile objections): `docs/security_review_internal.md`
- Threat model (assumptions + scope): `docs/threat_model.md`

## Quick review checklist (for skeptics)
A reviewer should be able to confirm:
- There is no autonomy or background execution
- Consent is not brokered; the platform remains the source of truth
- Proposal and commit are never collapsed
- Refusals are deterministic and auditable (category + reason_code)
- Failures result in “no action taken” with no automatic retries
- Breaking invariants invalidates the system

## Versioning & change policy
- Month 11 artifacts are semantic hardening and are treated as lockable constraints
- Month 12 focuses on external intelligibility (clarity, not new power)
- Any change that increases power requires explicit invariant revision

---
Status: Month 12 — External Intelligibility (Doc clarity only)
Change policy: clarification-only changes allowed; no power expansion without invariant revision
Review expectation: written to survive adversarial review
