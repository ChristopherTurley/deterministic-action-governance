# Enterprise Demo Surfaces Pointer (Non-Artifact)

Purpose
- Provide a clear pointer to enterprise demo surfaces (UI/sidecar/docker) without contaminating the commercial artifact.

Non-negotiable
- The commercial artifact is `main`.
- Enterprise demo surfaces must never be merged into `main`.
- Enterprise demo surfaces are not evidence for the commercial bundle and do not expand commercial claims.

Enterprise branch
- `enterprise_surfaces_preserved_20260120T180918Z`

Enterprise probe contract (demo-only)
- `/healthz` returns 200 without auth
- `/api/status` returns 200 with `Authorization: Bearer <UI_ADMIN_TOKEN>`

Reminder
- Procurement, acceptance, and evidence are governed by:
  - `v2/docs/public/EVALUATOR_RUNBOOK_V1.md`
  - `v2/docs/public/EVIDENCE_BUNDLE_V1.md`
  - `bash v2/tools/run_commercial_suite_v1.sh`

(END)
