# REFERENCE FREEZE (AUTHORITATIVE)

Status
- This repository is in REFERENCE FREEZE.
- It is a stable reference artifact for deterministic action governance.
- It is not a product roadmap, not a feature surface, and not an experimentation space.

What Is Frozen
The following are frozen and must not change without an explicit governance decision:

1) Core Invariants
- Proposal -> decision -> explicit commit
- Default-deny side effects
- Refusal and inaction are correct outcomes
- Deterministic state transitions via reducer commits only
- No background execution, retries, escalation, or autonomy

2) Execution Boundaries
- Entrypoints remain sterile airlocks (no args, no env branching, no modes).
- No intelligence or discretion exists before governance is active.

3) Hats and Coats
- Hats never execute and never escalate authority.
- Day-side hats may explain, simulate, or reflect only.
- Coats map reason codes to language and do not decide.
- Removing a hat or coat must never change execution behavior.

4) Repo Posture
- This repo remains a reference artifact.
- It must not drift toward a product, agent, assistant, or automation platform.

What Changes Are Explicitly Rejected
The following are categorically out of scope post-freeze:

- Adding autonomy, background execution, retries, or schedulers
- Adding optimization, advice, or recommendation logic
- Adding configuration flags or modes that affect authority
- Adding UI, workflows, or product surfaces
- Adding “just one more improvement” without governance review

Allowed Post-Freeze Changes (Narrow)
The only changes allowed after reference freeze are:

- Fixing factual inaccuracies in documentation
- Clarifying language to remove ambiguity or misuse risk
- Correcting typos
- Adding explicitly approved, non-executing reference artifacts
- Security or integrity fixes that reduce capability (never increase it)

Interpretation Rule
- Ambiguity must be resolved toward refusal and non-execution.
- If a proposed change could plausibly increase actionability, it is rejected.

If There Is Ever Doubt
- Assume the freeze holds.
- Assume refusal is correct.
- Assume less capability is safer.

This document is itself frozen.

────────────────────────
You are on the Evaluator Track

Next: docs/invariants.md
Return to start: docs/START_HERE.md
