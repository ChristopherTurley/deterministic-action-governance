# Claims and Non-Claims v1 — VERA Commercial Bundle v1 (LOCKED)

Purpose
- Prevent implied promises.
- Make the contracted scope unambiguous for executives, legal, procurement, and auditors.

Core claim (what VERA is)
VERA Commercial Bundle v1 is a **governance verification artifact** that enables:
- deterministic evaluation of governance decision boundaries
- deterministic replay against canonical scenarios and reference receipts
- offline verification via Device-B tooling
- evidence generation suitable for audit/board/regulatory review

Verification claim (how it is proven)
- Proof is the commercial suite: `bash v2/tools/run_commercial_suite_v1.sh`
- PASS/FAIL is objective and captured as evidence per:
  - `v2/docs/public/EVALUATOR_RUNBOOK_V1.md`
  - `v2/docs/public/EVIDENCE_BUNDLE_V1.md`

Non-claims (explicit exclusions)
VERA Commercial Bundle v1 does NOT provide:
- SaaS, hosting, or managed service
- runtime enforcement or production integration
- middleware/proxy/sidecar “plug-in” deployment as a deliverable
- dashboards for policy authoring or rule toggling as part of the commercial artifact
- cryptographic signing guarantees or “tamper-proof” claims beyond deterministic replay + verifier evidence
- latency or performance guarantees (no sub-200ms claims; not an inline gate)
- legal/clinical/trading/operational advice
- compliance certification or regulatory approval guarantees

Acceptance (objective)
Acceptance is satisfied if:
- Device-B verifier completes successfully using the shipped artifact
- deterministic replay outputs match shipped reference receipts (per verifier)
- the commercial suite exits 0

Enterprise demo surfaces
- UI/sidecar/docker demos may exist on a separate branch.
- They are explicitly non-artifact and must not be used to expand commercial reliance.

(END)
