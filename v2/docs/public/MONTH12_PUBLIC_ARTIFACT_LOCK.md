# Month 12 — Public Artifact Lock (Apple Gap + Demo Harness)

This repository is a **governance reference artifact**: it demonstrates deterministic decision boundaries, fail-closed behavior, and audit-legible output.
It does **not** execute side effects, call external services, or perform automation.

## Canonical Locked State
- Tag: `VERA_v2_QUICK_PROOF_LOCKED_SURFACES_GREEN_20260115`

## What Month 12 is (and is not)

### Month 12 IS
- A clean, engineer-readable public artifact
- A deterministic demo harness that proves:
  - proposal vs commit semantics
  - drift detection → `REQUIRE_RECOMMIT`
  - unknown hats fail-closed
  - reason codes are stable and namespaced
  - the coat renders decisions without changing outcomes
- An Apple-facing “gap map” showing what App Intents / Apple Intelligence lack:
  - explicit decision boundary surfaces
  - drift detection & recommit semantics
  - audit receipts for operator-confirmed actions
  - refusal being first-class (not “error”)

### Month 12 IS NOT
- A product
- An agent
- An automation layer
- A capability repo

## Reader Path (10 minutes total)
1) Start here:
- `README.md`
- `v2/docs/demo_index.md`

2) Run the proofs:
- `python3 -m pytest -q`
- `v2/demo/scripts/run_all_demos.sh`

3) Read the Month 12 public docs:
- `v2/docs/public/APPLE_GAP_MAP_MONTH12.md`
- `v2/docs/public/ONE_PAGER.md`
- `v2/docs/public/INVESTOR_NARRATIVE.md`
- `v2/docs/public/DEMO_SCRIPT_VERBAL.md`

## Demo Guarantees (what must remain true)
- Same input → same decision
- No background execution
- Refusal is a successful outcome
- Drift is detectable and forces explicit recommit
- Coats never change decisions (render only)

## Acceptance Criteria (Month 12 complete when)
- `pytest` is green
- `run_all_demos.sh` completes
- `demo_index.md` is navigable and current
- Apple gap map is present and points to deterministic proofs
