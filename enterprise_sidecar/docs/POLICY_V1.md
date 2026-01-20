# Sidecar Policy v1 (Config-Only Governance)

The enterprise sidecar evaluates proposals against a policy document.
Policy is configuration only (no code edits, no DSL).

Design goals:
- Flat rules (simplicity over coverage)
- Deterministic evaluation
- Fail-closed default posture
- Clear rule IDs and refusal codes

Admin UI may:
- Toggle rules on/off
- Adjust numeric thresholds
- Version policies

Admin UI must not:
- Modify enforcement code
- Override decisions
- Execute actions

Evaluation outputs:
- ALLOW/REFUSE
- refusal_code (if refused)
- rule_ids that fired
- signed receipt
