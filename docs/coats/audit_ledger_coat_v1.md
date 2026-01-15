# Audit / Ledger Coat v1 — Explanation Specification (Non-Decisional)

Status
- Version: v1
- Authority: NONE
- Execution: FORBIDDEN
- Binding: NON-BINDING
- Scope: Explanation only

Purpose
The Audit / Ledger Coat exists to explain how events are recorded and
why those records are trustworthy for later review.

It describes the existence and properties of the ledger,
not the meaning or quality of its contents.

Non-Goals (Hard Prohibitions)
This coat MUST NOT:
- analyze outcomes or performance
- summarize trends or metrics
- recommend review actions
- suggest optimizations or corrections
- interpret intent or effectiveness
- collapse record-keeping into evaluation

Inputs (Only)
- ledger identifiers
- event identifiers
- causality references (event ordering, parent-child relationships)

The coat does not inspect content beyond what is necessary
to explain recording mechanics.

Outputs (Only)
- human-readable explanation text that:
  - states that events were recorded
  - states that records are append-only
  - states that ordering and causality are preserved
  - affirms immutability after recording

Example Output Characteristics
Allowed:
- “The event was recorded in the append-only ledger.”
- “Once recorded, ledger entries are not modified or deleted.”
- “Event ordering preserves causal relationships.”

Disallowed:
- “This was a good decision…”
- “Performance improved…”
- “You should review…”
- “Consider changing…”

Tone Requirements
- Declarative
- Neutral
- Final
- Non-judgmental

The ledger is described as a fact, not a tool for advice.

Removal Safety
Removing the Audit / Ledger Coat MUST:
- not change any recording behavior
- not affect causality or ordering
- not change execution or refusal behavior
- only remove explanatory clarity

If removing this coat changes behavior, the system is invalid.

Interpretation Rule
If explanation risks sounding evaluative,
default to stating recording properties only.

This document is a reference artifact and is frozen at v1.
