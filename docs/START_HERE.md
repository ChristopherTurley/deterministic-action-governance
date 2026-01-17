# START HERE — VERA Deterministic Governance (90 seconds)
VERA is a governance-only reference artifact that demonstrates a missing primitive in modern AI systems:
Proposal → deterministic decision → auditable receipt → (optional) explicit operator commit
This repo does not automate anything and does not execute side effects.
It exists to prove that:
refusal and inaction are first-class outcomes
decisions are deterministic (re-runable and diffable)
every decision produces an auditable receipt surface
If you only do one thing: run the invariants.
1) Run the invariant suite (must be green)
python3 -m pytest -q
2) Run the canonical demos (no side effects)
See:
v2/docs/demo_index.md
Recommended:
python3 -m v2.demo.universal_governance_demo_v1
3) Trading Gate Pack v1 (Device B offline bundle)
Bundle source (repo):
v2/nda/trading_gate_pack_v1
Build the Device B zip (generated artifact):
cd v2/nda/trading_gate_pack_v1
./scripts/make_device_b_zip.zsh
Verify offline on a second machine (Device B):
rm -rf /tmp/trading_gate_pack_v1_audit
mkdir -p /tmp/trading_gate_pack_v1_audit
unzip -q dist/trading_gate_pack_v1_device_b.zip -d /tmp/trading_gate_pack_v1_audit
cd /tmp/trading_gate_pack_v1_audit

python3 tools/validate_receipt.py reference/trading_precheck_mixed.receipt.json schema/trading_hat_receipt_schema_v1.json policy/trading_hat_rules_v1.json
./scripts/diff_receipts.zsh reference/trading_precheck_mixed.receipt.json reference/trading_precheck_mixed.receipt.json

echo "OK: Device B audit passed"
Any mismatch or failure is a correct stop signal.
