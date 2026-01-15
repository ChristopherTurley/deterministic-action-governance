# REPO MAP (AUTHORITATIVE READER GUIDE)

Purpose
- This repository is a reference artifact that documents deterministic action governance.
- It is not a product, not an agent, and not a platform for autonomy.

Non-Negotiable Invariants
- Proposal -> decision -> explicit commit
- Default-deny side effects
- Refusal and inaction are correct outcomes
- Deterministic state transitions via reducer commits only
- No background execution, no retries, no escalation
- Any single refusal blocks execution

Where Execution Begins (Airlock)
- Entry points must be sterile airlocks: no flags, no branching, no intelligence.
- Entrypoints that parse args, read environment state, or select modes are incompatible with this governance posture.

Canonical vs Non-Canonical Areas
Canonical (authoritative, governance-bearing)
- docs/ : Reader-facing reference docs and governance explanations
- spec/ : Specification artifacts (declarative, not executable authority)

Non-canonical (supporting, never authority-bearing)
- demo/ : Demonstrations only. Demos must showcase refusal and restraint.
- vera_v2_public_deposit/ : Historical or staging deposit of materials for reference.
  - This folder is not an execution surface and is not authoritative.
  - Contents here must never be treated as "the system" unless explicitly promoted by a separate governance decision.

Hats (Governance Layers)
- Hats never execute.
- Hats never escalate authority.
- Hats compose only by increasing constraint.
- Day-side hats are strictly non-binding intelligence (explain, simulate, reflect).
- Day-side hats must not advise, recommend, optimize, or instruct action.

Coats (Explanation Only)
- Coats map reason codes to language.
- Coats do not decide.
- Removing a coat must never change execution behavior.
- Coats must not soften outcomes or change refusal clarity.

What Reviewers Should Check First
1) Entry points remain sterile (no discretion before governance)
2) No side effects without explicit commit and attributable authority
3) Refusal paths are clearer than execution paths
4) Hats contain no advice or optimization language
5) Deposit and demos cannot be mistaken for canonical behavior

Misuse Resistance
- If a reader can plausibly interpret any area as enabling autonomy, that is a documentation failure.
- The correct fix is improved boundary labeling, not more capability.

If Anything Conflicts
- The core invariants above win.
- Ambiguity must be resolved toward refusal and non-execution.
