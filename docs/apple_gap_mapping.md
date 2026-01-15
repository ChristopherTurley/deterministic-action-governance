# Apple Platform Gap Mapping (Neutral)

This document maps existing Apple platform capabilities to the governance primitives VERA expresses.
It is descriptive, not prescriptive.

---

## What Apple platforms express well

### App Intents / Siri / Shortcuts
- Declarative action exposure
- Parameterized intent handling
- Permission-scoped execution
- Strong platform consent flows
- User-facing discoverability

### Apple Intelligence / AI stacks
- Natural language interpretation
- Contextual suggestion
- On-device privacy controls
- Model safety boundaries

These systems are optimized for **capability exposure** and **user experience**.

---

## What is intentionally not expressed as a primitive

The following concepts are not first-class primitives in current Apple stacks (by design):

### Proposal vs commit separation
- User intent is typically interpreted and executed in a single flow
- There is no durable, auditable “proposal” artifact distinct from execution

### Fail-closed governance
- Safety is often implemented via allowlists or permissions
- There is no generic, reusable “refusal taxonomy” with reason codes

### Explicit authority artifacts
- Authority is inferred from context, UI flow, or permission state
- There is no portable artifact that says: “this action was explicitly committed by the user”

### Drift visibility
- Systems optimize for success paths
- Drift prevention is implicit, not externally auditable

---

## The gap VERA occupies

VERA does not replace platform capabilities.
It introduces a **governance layer above them**.

Specifically, VERA provides:
- A durable proposal artifact
- A deterministic decision outcome (refuse / fail / unavailable / allow-for-commit)
- An explicit commit boundary owned by the user
- Auditable refusal and failure semantics
- Explicit non-goals that prevent authority creep

This gap exists independently of any specific platform.

---

## Why this is complementary, not competitive

- App Intents define *what an app can do*
- VERA governs *whether an action should be allowed at all*
- Platform consent remains authoritative
- Execution remains external

VERA operates downstream of consent and upstream of execution.

---

## Non-goals (important)

This mapping does not claim:
- That existing platforms are insufficient
- That VERA should replace native frameworks
- That governance should be centralized

It only identifies a missing primitive: **deterministic action governance**.

---

Status: Month 12 — Apple Gap Mapping
Change policy: clarification-only changes allowed; no power expansion without invariant revision
Review expectation: written to survive adversarial review
