# VERA — Deterministic Action Governance Engine

## What this repository is
- Deterministic, fail-closed action governance layer
- Separates: proposal → decision → explicit commit
- Designed for auditability and drift resistance

## What this repository is not
- Not an agent
- Not autonomous
- Not a UI product
- Not a background task runner
- Not a policy/ethics engine
- Not a permissions broker

## High-level architecture (non-exhaustive)
- Inputs are treated as untrusted proposals
- Decisions are explicit, explainable, and logged
- No execution occurs without explicit user commit
- Refusals are preferred over unsafe action

## Non-goals (explicit)
- No UI work
- No “soft approvals”
- No implicit authority
- No background execution
- No v1 behavior changes

## How to read the docs
- Start with `docs/invariants.md`
- Then read `docs/threat_model.md`
- Then read `docs/refusal_model.md`
- Then read `docs/security_review_internal.md`
- Finally read `docs/failure_modes.md`

## Versioning & freeze philosophy
- Month 11 focuses on semantic hardening and skeptical-proof clarity
- Documentation changes must not expand power unless invariants are revised

---
Status: Month 11 — Semantic Hardening  
Change policy: clarification-only changes allowed; no power expansion without invariant revision  
Review expectation: written to survive adversarial review
