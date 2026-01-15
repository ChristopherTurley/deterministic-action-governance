# Evaluate This Repository

This repository documents a deterministic action governance model for AI-assisted systems that can perform actions.

It is written to be evaluated by:
- platform and systems engineers
- security and trust teams
- product owners responsible for execution semantics

It does not make claims about intelligence quality, UX, or product strategy.

---

## 90-second quick scan

Read these in order:

1) Root README
- `README.md`

2) Constitution
- `docs/invariants.md`

3) Refusal semantics
- `docs/refusal_model.md`

4) Failure behavior
- `docs/failure_modes.md`

If any of the above imply autonomy or background execution, the model is not being represented correctly.

---

## 5-minute engineer evaluation path

### 1) Confirm the core lifecycle is never collapsed
Use the timeline model:
- `docs/ledger_timeline_model.md`

You should be able to identify:
- proposal
- decision
- commit
as distinct and auditable phases.

### 2) Confirm refusals are a correct outcome
Use the refusal taxonomy:
- `docs/refusal_model.md`

A refusal must have:
- category
- reason_code
- clear next action or none
and must produce no partial execution.

### 3) Confirm failures fail closed
Use the failure narratives:
- `docs/failure_modes.md`

A failure must:
- produce no action taken
- perform no retries
- perform no background recovery

### 4) Confirm security assumptions are explicit
Use:
- `docs/threat_model.md`
- `docs/security_review_internal.md`

The security review is intentionally hostile. It exists to surface objections early.

---

## Reproducible demonstration

If the demo harness exists in this repo, use:
- `docs/demo_harness_walkthrough.md`
- `v2/docs/demo_index.md`

Expected result:
- deterministic output
- auditable decision records
- explicit commit required for any action

If the demo harness does not exist or is not runnable in your environment, evaluate the docs as a specification.

---

## What to look for as a reviewer

You should be able to answer:

- Is any action executed without an explicit, synchronous commit
- Are refusals deterministic and logged as first-class outcomes
- Are failures surfaced distinctly from refusals
- Does the system prefer doing nothing over acting under unclear authority
- Are permission and identity decisions delegated to the platform and not brokered here
- Are non-goals explicit and enforced

If any answer is unclear, treat that as a defect in documentation clarity and request clarification.

---

## Status

This repository documents completed work as of the current tags.
Ideas and future directions are explicitly separated from current guarantees.
