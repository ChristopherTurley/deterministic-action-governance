# Refusal Coat v1 — Explanation Specification (Non-Decisional)

Status
- Version: v1
- Authority: NONE
- Execution: FORBIDDEN
- Binding: NON-BINDING
- Scope: Explanation only

Purpose
The Refusal Coat exists to explain why no action occurred.
It translates refusal reason codes into clear, non-negotiable language
without altering outcomes or authority.

A refusal is a correct and intentional outcome.

Non-Goals (Hard Prohibitions)
This coat MUST NOT:
- decide, allow, or deny anything
- soften or negotiate refusals
- suggest alternative actions
- recommend retries or rephrasing
- imply future execution
- collapse explanation into advice
- escalate authority or override constraints

Inputs (Only)
- refusal reason codes
- recorded proposal metadata
- governance boundary identifiers

The coat does not inspect intent, context, or user goals.

Outputs (Only)
- human-readable explanation text that:
  - states that no action occurred
  - identifies the blocking boundary
  - affirms correctness of refusal

Example Output Characteristics
Allowed:
- “No action was taken because the proposal exceeded the permitted authority.”
- “The request was refused due to a time-bound restriction.”
- “Execution did not occur because the system was in a non-executing state.”

Disallowed:
- “You could try…”
- “If you rephrase…”
- “Next time you may want to…”
- “Consider doing…”

Tone Requirements
- Declarative
- Neutral
- Final
- Non-negotiable

Refusals must not sound apologetic, persuasive, or helpful.

Removal Safety
Removing the Refusal Coat MUST:
- not change any refusal outcome
- not change any execution behavior
- not change authority requirements
- only reduce the availability of explanatory text

If removing this coat changes behavior, the system is invalid.

Interpretation Rule
If there is ambiguity between:
- clarity vs softness
- explanation vs guidance

Choose clarity and refusal.

This document is a reference artifact and is frozen at v1.
