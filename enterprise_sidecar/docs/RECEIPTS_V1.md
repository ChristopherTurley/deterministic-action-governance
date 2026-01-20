# Sidecar Receipts v1 (Audit Proof)

A receipt is emitted for every evaluation performed by the enterprise sidecar.

Receipts are:
- Deterministic (derived from proposal + policy + engine version)
- Tamper-evident (hash-chained)
- Verifiable offline (Ed25519 signature)

Receipts prove:
- What was evaluated (by hash)
- Which policy version was applied (by hash)
- The deterministic decision (ALLOW/REFUSE) and refusal code
- That the record was not modified after emission (signature + chain)

Receipts do NOT:
- Execute actions
- Provide advice
- Replace organizational policy or legal review

Verification steps:
1) Verify schema conformance
2) Verify signature against the published public key
3) Verify chain continuity using prev_receipt_id
