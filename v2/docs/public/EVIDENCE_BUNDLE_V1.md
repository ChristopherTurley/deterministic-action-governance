# Evidence Bundle v1 — Deterministic Retention List (LOCKED)

Purpose
- Define the exact artifacts an evaluator/auditor retains as evidence of verification.
- This is a deterministic list. Additions require an explicit version bump.

Scope
- Commercial artifact on branch `main` only.
- Enterprise demo surfaces are out of scope and must not be included in evidence for the commercial bundle.

Evidence Bundle v1 (retain all items)

A) Repository identity
- `git remote -v`
- `git rev-parse HEAD`
- `git tag --points-at HEAD`
- `git show -s --format=fuller HEAD`
- `git status --porcelain` (must be empty)

B) Commercial proof execution
- Full stdout/stderr from: `bash v2/tools/run_commercial_suite_v1.sh`
- The script exit code (0 = PASS; non-zero = FAIL)

C) Device-B verification proof (as produced by the suite)
- Device-B verifier output (pass/fail)
- The Device-B manifest file used for verification:
  - `v2/device_b/MANIFEST.json`
- Any verifier reports emitted by the suite (retain exact filenames produced)

D) Deterministic reference evidence (commercial bundle)
Retain the shipped deterministic reference materials for each included hat:
- `v2/reference/<hat>/scenarios.json`
- `v2/reference/<hat>/reference_receipts.json`

Included hats are defined by:
- `v2/docs/public/COMMERCIAL_BUNDLE_V1.md`

E) Environment metadata (for reproducibility)
- `uname -a`
- `python3 --version`

Interpretation rules (non-negotiable)
- Evidence is valid only when produced from `main` and an identified commit/tag.
- If any step fails, retain outputs and treat evaluation as FAIL.
- Do not patch or modify the artifact during evaluation.

(END)
