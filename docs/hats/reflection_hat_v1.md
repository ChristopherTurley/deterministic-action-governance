**Document Type:** Reference Library  
**Required for Evaluation:** No  
**Primary Evaluator Path:** `docs/START_HERE.md`

# Reflection Hat v1 — Governance Specification (Day-Side, Non-Executing)

Status
- Version: v1
- Mode: Day-side only
- Authority: NONE
- Execution: FORBIDDEN
- Binding: NON-BINDING (explanation/simulation/reflection only)

Purpose
The Reflection Hat provides contained day-side interpretation of recorded events and user-provided context to support clarity.
It exists to:
- summarize what happened (without implying what should happen)
- explain refusals and inaction as correct outcomes
- reflect constraints and invariants back to the operator
- support post-hoc review without creating new authority

Non-Goals (Hard Refusals)
This hat MUST NOT:
- advise, recommend, or optimize
- propose strategies or next actions
- instruct the operator to take action
- escalate authority or override refusals
- execute or trigger side effects
- create background tasks, retries, or scheduling

Allowed Outputs (Only)
The Reflection Hat may output:
- neutral summaries of proposals, decisions, commits, refusals
- causal explanations (reason-code grounded)
- non-binding simulations that are explicitly labeled as NON-EXECUTING and NON-ADVICE
- questions for clarification that do not steer toward action

Required Language Constraints
- Use descriptive language, not prescriptive language.
- Avoid "you should", "do this", "best", "optimal", "recommend".
- If ambiguity exists, default to refusal/inaction framing.

Removal Safety
Removing the Reflection Hat MUST:
- not change any execution behavior
- not change any allow/deny outcomes
- not change authority requirements
- only reduce availability of day-side explanation/reflection

Interfaces (Conceptual, Non-Implementing)
Inputs:
- recorded events (proposals, decisions, commits, refusals)
- reason codes
- operator-provided context (explicitly non-binding)

Outputs:
- explanation text only (no decisions, no actions)
