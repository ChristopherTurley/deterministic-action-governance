**Document Type:** Reference Library  
**Required for Evaluation:** No  
**Primary Evaluator Path:** `docs/START_HERE.md`

# Boundary / Safety Coat v1 — Explanation Specification (Non-Decisional)

Status
- Version: v1
- Authority: NONE
- Execution: FORBIDDEN
- Binding: NON-BINDING
- Scope: Explanation only

Purpose
The Boundary / Safety Coat exists to explain which safety or governance
boundary blocked an action and why that boundary exists.

Boundaries are intentional and protective, not obstacles to work around.

Non-Goals (Hard Prohibitions)
This coat MUST NOT:
- decide, allow, or deny anything
- suggest how to bypass a boundary
- recommend parameter changes
- imply that boundaries are negotiable
- suggest retries, rephrasing, or escalation
- infer user intent or urgency

Inputs (Only)
- boundary identifiers (time, scope, role, state, policy)
- refusal reason codes
- recorded system state at decision time

Outputs (Only)
- human-readable explanation text that:
  - names the boundary that applied
  - states that the boundary is enforced by design
  - affirms correctness of inaction/refusal

Example Output Characteristics
Allowed:
- “No action occurred because the system was in a non-executing state.”
- “The request was blocked by a time-bound safety restriction.”
- “Execution was prevented by a scope boundary.”

Disallowed:
- “You can change the setting…”
- “If you try later…”
- “Adjust the scope…”
- “Ask for an override…”

Tone Requirements
- Declarative
- Neutral
- Final
- Non-negotiable

Boundaries must be described as fixed protections, not flexible rules.

Removal Safety
Removing the Boundary / Safety Coat MUST:
- not change any execution behavior
- not change any refusal behavior
- not change boundary enforcement
- only remove explanatory clarity

If removing this coat changes behavior, the system is invalid.

Interpretation Rule
If explanation could be read as guidance or workaround,
default to stating boundary enforcement and finality.

This document is a reference artifact and is frozen at v1.
