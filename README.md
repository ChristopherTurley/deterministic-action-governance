# Deterministic Action Governance (Commercial Bundle v1)

This repository is a **governance-only verification artifact**.
It is designed for procurement, audit, and evaluator readability.

This is NOT:
- a product
- SaaS
- an automation system
- an integration layer
- a runtime enforcement engine

## Start Here (reader ladder)

1) What you are buying (bundle definition)
- `v2/docs/public/COMMERCIAL_BUNDLE_V1.md`

2) Evaluator front door (repo map)
- `v2/docs/public/REPO_MAP_COMMERCIAL_V1.md`

3) How to verify (deterministic procedure)
- `v2/docs/public/EVALUATOR_RUNBOOK_V1.md`

4) What evidence to retain (auditor bundle)
- `v2/docs/public/EVIDENCE_BUNDLE_V1.md`

5) Prove it (one command)
- `bash v2/tools/run_commercial_suite_v1.sh`

## Procurement packet (commercial)
- License: `v2/legal/VERA_COMMERCIAL_BUNDLE_V1_LICENSE.md`
- Procurement cover memo: `v2/sales/PROCUREMENT_COVER_MEMO_V1.md`
- Compliance-grade sales brief: `v2/sales/COMPLIANCE_GRADE_SALES_BRIEF_V1.md`

Acceptance is objective:
- Device-B verifier passes and replay matches shipped reference receipts.

## Enterprise demo surfaces (explicitly non-artifact)
Enterprise UI / sidecar / docker surfaces are intentionally **not** part of the commercial artifact on `main`.
They live on a separate branch and must not be used as evidence of the commercial bundle.

See:
- `v2/docs/public/ENTERPRISE_SURFACES_POINTER.md`
