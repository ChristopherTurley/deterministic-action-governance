# What VERA Will Never Do

This document is a **hard constraint list**.
If any item below is violated, the system is no longer VERA.

This is not aspirational.
This is not configurable.
This is not negotiable.

---

## Authority & Control

VERA will never:
- Act without an explicit, synchronous user commit
- Infer permission, intent, or approval
- Reuse prior approvals without re-commit
- Delegate commit authority to itself or others
- Chain commits across actions
- Decide “on behalf of” the user

If the user cannot clearly say *“I did this”*, the action cannot occur.

---

## Autonomy & Execution

VERA will never:
- Execute actions autonomously
- Perform background execution
- Schedule or delay execution on its own
- Retry actions automatically after refusal or failure
- Escalate from suggestion to action without a commit
- Perform “best effort” execution

All execution is external.
All execution is explicit.

---

## Permissions & Consent

VERA will never:
- Grant permissions
- Request permissions
- Store permissions
- Proxy permissions
- Reinterpret platform consent
- Bypass native consent flows

Consent always belongs to the platform.
VERA remains downstream of consent.

---

## Scope & UI

VERA will never:
- Design or render UI
- Add overlays, widgets, or visual controls
- Blur system logic with presentation
- Expand scope silently
- Perform work explicitly marked out of scope

UI is not a backdoor for authority.

---

## Determinism & Safety

VERA will never:
- Fail open
- Guess when uncertain
- Use heuristics to bypass explicit rules
- Introduce non-deterministic behavior
- Collapse proposal, decision, and commit boundaries
- Optimize for convenience over correctness

Ambiguity results in refusal.

---

## Logging & Auditability

VERA will never:
- Hide refusals
- Mask failure reasons
- Suppress audit logs for cleanliness
- Perform unlogged side effects
- Enrich logs with inferred or speculative data

Logs exist to preserve accountability, not aesthetics.

---

## Version Integrity

VERA will never:
- Change frozen v1 behavior
- Modify locked semantics without explicit revision
- Expand power without invariant review
- Quietly reinterpret existing guarantees

If an invariant must change, it must be stated openly.

---

## Product Framing

VERA will never:
- Present itself as an agent
- Claim autonomous reasoning
- Market “intelligence” over governance
- Promise outcomes
- Replace user responsibility

VERA is a governance layer, not a decision-maker.

---

## Final Rule

If a future feature requires violating anything above,
that feature is forbidden.

---

Status: Month 11 — Explicit Non-Goals
Change policy: clarification-only changes allowed; no power expansion without invariant revision
Review expectation: written to survive adversarial review
