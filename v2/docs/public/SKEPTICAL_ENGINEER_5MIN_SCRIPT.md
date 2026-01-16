# 5-Minute Skeptical Engineer Demo Script (Canonical)

Audience
- senior engineers
- platform reviewers
- security/risk reviewers

Goal
Prove this repository is a governance-only reference artifact:
- deterministic evaluation path
- enforcement via tests
- refusal and fail-closed semantics
- platform gap narrative without execution

Constraints
- No automation
- No side effects
- No background behavior

---

## 0:00–0:20 Frame
Say:
“This repository is governance-only. It does not automate. It proves that AI action governance can be deterministic, fail-closed, and auditable.”

Open:
- README.md

---

## 0:20–0:50 Canonical evaluator path
Say:
“There’s exactly one canonical evaluator track. No branching.”

Open:
- docs/START_HERE.md

Point at:
- Lane A evaluator track list

---

## 0:50–1:30 Run the proof
Run:
- pytest -q

Say:
“These tests enforce the claims. If the repo drifted into side effects or nondeterminism, this goes red.”

---

## 1:30–2:30 Refusal is first-class
Open:
- docs/refusal_model.md

Optional proof anchors:
- v2/tests/test_unknown_hat_fail_closed_v1.py
- v2/tests/test_domain_hats_registered_fail_closed_v1.py

Say:
“Unknown domains do not degrade gracefully. They refuse deterministically. Refusal is a correct outcome.”

---

## 2:30–3:45 Platform gap
Open:
- docs/platform_gaps/APPLE_GAP_MAP_v2.md
- docs/platform_gaps/APPENDIX_GOVERNANCE_CANNOT_BE_BOLTED_ON.md

Say:
“This is the platform pressure point: current platforms don’t provide strong, deterministic action governance boundaries.”

---

## 3:45–5:00 Hard boundaries
Open:
- docs/vera_will_never.md

Say:
“These constraints are the point. This repo is meant to be cloned and trusted without trusting me.”

Stop.
