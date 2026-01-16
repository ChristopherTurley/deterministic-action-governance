# START HERE — Evaluator Track

This is the **canonical** evaluator path. It is intentionally linear.

## Lane A — Evaluator Track (7 files)
1) `docs/START_HERE.md`
2) `docs/REFERENCE_FREEZE.md`
3) `docs/invariants.md`
4) `docs/refusal_model.md`
5) `docs/platform_gaps/APPLE_GAP_MAP_v2.md`
6) `v2/docs/demo_index.md`
7) `v2/docs/public/DEMO_SCRIPT_VERBAL.md`

## What to run
- `pytest -q`

## Canonical demo entry
- `v2/docs/demo_index.md`


# VERA — Start Here (Required Onramp)

VERA is a **deterministic execution governance layer**, not an assistant.
It exists to prove (with tests + reproducible scenarios) that:
- execution is never implicit
- refusal is first-class and correct
- behavior is reproducible across machines
- the public artifact has **no side effects**
- private execution is segregated from public proof

This repository is intentionally conservative.
**Refusal is success. Inaction is correct.**

## Required Reading Order (Non-Optional)

If you read only one file, read this.
If you read three files, read the following in order:

1. `docs/START_HERE.md`
2. `docs/vera_will_never.md`
3. `docs/invariants.md` and `docs/refusal_model.md`

All conclusions about VERA are invalid unless you read those.

## Authority Map (What Wins In A Conflict)

- `v2/docs/` is the **canonical specification tied to code and tests**.
- `docs/` is **conceptual + narrative** and must not contradict `v2/docs/`.
- Tests in `v2/tests/` are the final enforcement layer.
In case of conflict: **tests win**, then `v2/docs/`, then `docs/`.

## Quick Verification (Proof First)

Run the suite and confirm VERA’s locked surfaces stay side-effect free:

- `pytest -q` must be green
- Key enforcement tests:
- `v2/tests/test_no_side_effect_imports_in_locked_surfaces.py`
- `v2/tests/test_domain_hats_registered_fail_closed_v1.py`
- `v2/tests/test_unknown_hat_fail_closed_v1.py`
- `v2/tests/test_coat_non_interference_v1.py`
- `v2/tests/test_month12_public_artifact_docs_present.py`

## Public Reader Pack (Skeptic Bundle)

Start here for a fast external evaluation:
- `v2/docs/public/README_PUBLIC.md`
- `v2/docs/public/ONE_PAGER.md`
- `v2/docs/public/DEMO_SCRIPT_VERBAL.md`
- `v2/docs/public/MONTH12_PUBLIC_ARTIFACT_LOCK.md`

## Platform Pressure Lane (Apple Gap Artifacts)

These are narrative artifacts that expose OS-level governance gaps.
They do not change VERA’s authority model:
- `docs/platform_gaps/APPLE_EXECUTION_GAP.md`
- `docs/platform_gaps/APPLE_GAP_MAP_v1.md`
- `docs/platform_gaps/APPLE_GAP_MAP_v2.md`
- `docs/platform_gaps/APPENDIX_GOVERNANCE_CANNOT_BE_BOLTED_ON.md`

## Credibility Signals (Read These If You Are Skeptical)

- `docs/HOSTILE_REVIEW.md`
- `docs/REMOVAL_SAFETY.md`

## What VERA Will Not Do

See: `docs/vera_will_never.md` (this is the hard boundary).

────────────────────────
You are on the Evaluator Track

Next: docs/REFERENCE_FREEZE.md
Return to start: docs/START_HERE.md
