# START HERE — VERA Deterministic Governance (90 seconds)

This repository is a governance-only reference artifact.

## 1) Run the invariant suite (must be green)
python3 -m pytest -q

## 2) Run the canonical demos (no side effects)
See:
- v2/docs/demo_index.md

## 3) Trading Gate Pack v1 (Device B offline bundle)
Bundle source:
- v2/nda/trading_gate_pack_v1

Build Device B zip (generated artifact, not committed):
cd v2/nda/trading_gate_pack_v1
./scripts/make_device_b_zip.zsh

Verify offline on a second machine:
unzip -q dist/trading_gate_pack_v1_device_b.zip -d /tmp/trading_gate_pack_v1_audit
cd /tmp/trading_gate_pack_v1_audit
python3 tools/validate_receipt.py reference/trading_precheck_mixed.receipt.json schema/trading_hat_receipt_schema_v1.json policy/trading_hat_rules_v1.json
./scripts/diff_receipts.zsh reference/trading_precheck_mixed.receipt.json reference/trading_precheck_mixed.receipt.json

Any mismatch or failure is a correct stop signal.
