# Authority Attribution Coat v1 — Explanation Specification (Non-Decisional)

Status
- Version: v1
- Authority: NONE
- Execution: FORBIDDEN
- Binding: NON-BINDING
- Scope: Explanation only

Purpose
The Authority Attribution Coat exists to explain authority boundaries.
It states clearly who had authority, who did not, and why no authority
was inferred, transferred, or escalated.

Authority attribution is descriptive, not permissive.

Non-Goals (Hard Prohibitions)
This coat MUST NOT:
- grant, deny, or modify authority
- suggest escalation or approval paths
- recommend how to gain authority
- imply that authority could be obtained by rephrasing
- soften refusals due to missing authority
- infer intent or urgency

Inputs (Only)
- authority identifiers present at proposal time
- role and scope identifiers
- recorded decision outcomes
- refusal reason codes related to authority

The coat does not inspect intent, sentiment, or goals.

Outputs (Only)
- human-readable explanation text that:
  - identifies which authority was present
  - identifies which authority was absent
  - states that no authority transfer occurred

Example Output Characteristics
Allowed:
- “No action was taken because the requesting entity lacked execution authority.”
- “Execution required operator authority, which was not present.”
- “Authority was limited to proposal submission; execution authority was not granted.”

Disallowed:
- “You can request approval…”
- “Ask an administrator…”
- “If you escalate…”
- “You may want to get permission…”

Tone Requirements
- Declarative
- Neutral
- Final
- Non-negotiable

Language must not imply that authority is negotiable or attainable within the system.

Removal Safety
Removing the Authority Attribution Coat MUST:
- not change any execution outcome
- not change any refusal behavior
- not change authority enforcement
- only remove explanatory clarity

If removing this coat changes behavior, the system is invalid.

Interpretation Rule
If explanation risks sounding like instruction or guidance,
default to stating absence of authority and finality.

This document is a reference artifact and is frozen at v1.
