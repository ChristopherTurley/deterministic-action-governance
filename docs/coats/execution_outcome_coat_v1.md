# Execution Outcome Coat v1 — Explanation Specification (Non-Decisional)

Status
- Version: v1
- Authority: NONE
- Execution: FORBIDDEN
- Binding: NON-BINDING
- Scope: Explanation only

Purpose
The Execution Outcome Coat exists to explain what did or did not occur
after an explicit commit attempt.

It must make the boundary between:
- proposal
- decision
- explicit commit
- refusal / inaction
unmistakable.

Non-Goals (Hard Prohibitions)
This coat MUST NOT:
- decide, allow, or deny anything
- imply execution occurred when it did not
- soften refusals or inaction
- suggest alternative actions or next steps
- recommend retries, rephrasing, or escalation
- infer intent, urgency, or goals

Inputs (Only)
- recorded events (proposal, decision, commit attempt, refusal)
- reason codes
- outcome identifiers (e.g., NO_EXECUTION, COMMIT_ACCEPTED, COMMIT_REFUSED)

Outputs (Only)
- human-readable explanation text that:
  - states whether any externally meaningful action occurred
  - distinguishes proposal from explicit commit
  - states finality (refusal/inaction is correct)

Example Output Characteristics
Allowed:
- “No action occurred. The system recorded a proposal but no explicit commit was accepted.”
- “An explicit commit was presented and refused. No externally meaningful action occurred.”
- “An explicit commit was accepted. The committed action was executed as recorded.”

Disallowed:
- “It looks like it ran…”
- “It probably executed…”
- “Try again…”
- “You should…”

Tone Requirements
- Declarative
- Neutral
- Final
- Non-negotiable

Removal Safety
Removing the Execution Outcome Coat MUST:
- not change any execution behavior
- not change any refusal behavior
- not change authority enforcement
- only remove explanatory clarity

If removing this coat changes behavior, the system is invalid.

Interpretation Rule
If explanation could be read as implying execution, it is invalid.
Default to stating "no externally meaningful action occurred" unless the recorded outcome explicitly indicates otherwise.

This document is a reference artifact and is frozen at v1.
