# REMOVAL SAFETY (HATS + COATS)

This document defines removal / disable safety invariants.
It adds no capability. It only constrains interpretation.

## Definitions
- Hat: governance layer that may interpret or explain within its scope, but never executes and never escalates authority.
- Coat: explanation-only layer that maps reason codes to language; it never decides.

## Non-Negotiable Removal Invariants

### Coat Removal (Explanation Layer)
Removing a coat MUST:
- not change any decision outcome
- not change any refusal/allow result
- not change authority requirements
- not introduce new execution paths
- not change state transition legality

Allowed effect of coat removal:
- less user-friendly messaging
- loss of phrasing polish
- unchanged underlying reason codes and outcomes

Fail condition:
- if removing a coat changes what happens (not just what is said), the system is invalid.

### Hat Removal (Governance Interpretation Layer)
Removing a hat MUST:
- not enable new execution
- not loosen constraints (removal cannot increase permission)
- not escalate authority
- not bypass refusal gates
- not change the deterministic core loop guarantees

Allowed effect of hat removal:
- less day-side interpretation/explanation/simulation in that domain
- unchanged core governance behavior

Fail condition:
- if hat removal increases actionability or reduces refusals, the system is invalid.

## Composition Safety
- Multiple hats must compose only by increasing constraint.
- Removing any hat from a multi-hat configuration must not make execution easier.
- Any single refusal blocks execution.

## How to Verify (read-only checks)
Run these from repo root:

A) Coats must not decide:
- search for coat code paths that return allow/deny decisions or mutate authority.
- coats may only transform reason codes -> text.

B) Hats must not execute:
- search hat-related code/docs for direct side-effect primitives or implicit commit language.
- hats must not contain "execute", "auto-commit", "implicit commit", or "bypass".

C) Removal must not reduce refusals:
- check docs explicitly state refusal/inaction as correct outcomes.
- ensure no language suggests "fallback execution" when hats/coats are absent.

Interpretation is fail-closed:
- if ambiguity exists, treat it as a violation and tighten documentation.
