# Commercial Bundle v1 — Repo Map (Evaluator Front Door)

This repository is a **procurement-safe governance reference artifact**.
It is **not** a runtime assistant, not an automation product, and contains **no executing capability** beyond deterministic verification tooling.

## Verify (one command)
Run:
- `bash v2/tools/run_commercial_suite_v1.sh`

Expected result:
- All checks PASS (commercial suite green)
- Device-B verifier OK
- No network required for verification

## What you are buying
**Commercial Bundle v1** contains five frozen hats:
- TRADING_HAT_V1
- EXECUTIVE_HAT_V1
- OPS_INCIDENT_HAT_V1
- HEALTHCARE_HAT_V1
- EDUCATION_HAT_V1

Each hat ships with:
- frozen spec (`v2/docs/hats/`)
- deterministic scenarios (`v2/reference/<hat>/scenarios.json`)
- deterministic reference receipts (`v2/reference/<hat>/reference_receipts.json`)
- replay tool (`v2/tools/run_<hat>.py`)
- freeze guard tests (`v2/tests/test_<hat>_freeze.py`)

## Folder meanings (why there are “many folders”)
- `v2/docs/` — canonical specs and public-facing explanations
- `v2/reference/` — deterministic scenarios + receipts (the “evidence”)
- `v2/device_b/` — offline verification (manifest + verifier)
- `v2/bundles/` — bundle snapshot locks (what counts as “included”)
- `v2/tests/` — invariants and lock guards (fail-closed)
- `v2/tools/` — deterministic generators/replayers (no execution)

## Procurement + legal
- `v2/legal/` — license + procurement rider
- `v2/sales/` — compliance-grade sales brief + cover memo

## Non-goals (explicit)
- no app / UI
- no integrations
- no background automation
- no “assistant runtime”

If you are looking for the original experimental runtime history:
- See branch: `archive_precommercial_20260117`
- Tag: `VERA_ARCHIVE_PRECOMMERCIAL_20260117`
