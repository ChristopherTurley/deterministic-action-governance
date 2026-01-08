# v2 Persistent Daily State (PDS) — Reducer Rules (Canonical)

PDS is NOT memory, embeddings, or chat history.
PDS is explicit state that makes VERA continuous, predictable, and trusted.

## Modes (explicit finite-state)
- IDLE
- INTAKE
- FOLLOWUP_OPEN
- FOLLOWUP_SCHEDULE

## Reducer principles (non-negotiable)
1) Deterministic: same input + same state => same output + same state_delta
2) Explicit: no hidden mutation; only through state_delta
3) Conservative: if uncertain, do not change state (trust > cleverness)
4) One-way safety: never delete user commitments unless explicitly commanded

## State transitions (minimum viable)
### IDLE → INTAKE
Trigger: input is a task capture, scheduling request, or "start my day"

### INTAKE → FOLLOWUP_OPEN
Trigger: v1 asks a clarifying question or opens a follow-up window

### FOLLOWUP_OPEN → FOLLOWUP_SCHEDULE
Trigger: user confirms details that allow schedule build / concrete action

### FOLLOWUP_* → IDLE
Trigger: followup expires OR action is complete and no further question remains

## Follow-up invariants
- Follow-up must NOT require unnecessary re-wake when within followup window.
- followup.until_utc is the only time authority.
- If followup.open is false, engine must behave as IDLE (no implicit context).

## Daily rollover
On local_date change:
- Close followup (open=false)
- Carry unfinished tasks forward into inbox or unfinished list (never silently delete)
- Reset active_context (conservative)

