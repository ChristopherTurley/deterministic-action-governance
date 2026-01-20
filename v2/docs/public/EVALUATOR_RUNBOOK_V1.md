# Evaluator Runbook v1 — VERA Commercial Bundle v1 (LOCKED)

Purpose
- Provide a deterministic, auditor-friendly procedure to verify the commercial artifact.
- This is a verification runbook, not a capability description.

Scope
- Applies only to the commercial artifact on branch `main`.
- Enterprise demo surfaces (UI/sidecar/docker) are explicitly out of scope and must not be used as evidence for the commercial bundle.

Authoritative proof command
- `bash v2/tools/run_commercial_suite_v1.sh`

Prerequisites
- git, bash, python3 available on the evaluator machine
- no network required for verification
- run from repository root

Procedure (deterministic)
1) Acquire repository
   - Clone from the official remote.
2) Confirm branch and cleanliness
   - Confirm you are on `main` and not in detached HEAD.
   - Confirm working tree is clean (no uncommitted changes).
3) Confirm lock tag
   - Confirm tag `DAG_COMMERCIAL_BUNDLE_V1_MAINLINE_LOCK_20260120` exists and points to the commit under evaluation.
4) Run the commercial proof suite
   - Execute: `bash v2/tools/run_commercial_suite_v1.sh`
5) Record evidence bundle (retain exactly these artifacts)
   - `git remote -v`
   - `git rev-parse HEAD`
   - `git tag --points-at HEAD`
   - `git status --porcelain` (must be empty)
   - `git show -s --format=fuller HEAD`
   - Full stdout/stderr from `bash v2/tools/run_commercial_suite_v1.sh`
   - Platform metadata: `uname -a`, `python3 --version`

Pass/Fail criteria (objective)
PASS if and only if:
- `bash v2/tools/run_commercial_suite_v1.sh` exits 0
- the suite reports all required checks passing
- no forbidden repo-root entries are present on `main`
- Device-B verification (as invoked by the suite) reports success

FAIL if any of the above conditions is not met.

Evaluator constraints
- Do not patch, “fix,” or modify the artifact during evaluation.
- If the suite fails, capture logs and treat the evaluation as FAIL.

Non-goals
- This runbook does not claim runtime enforcement, automation, or integration capability.
- This runbook does not provide legal, clinical, trading, or operational advice.

(END)
