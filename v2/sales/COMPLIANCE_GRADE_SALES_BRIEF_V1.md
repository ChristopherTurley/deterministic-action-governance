# VERA — Compliance-Grade Sales Brief v1 (LOCKED)

Date: 2026-01-17
Product: VERA Commercial Bundle v1 (Governance Verification Artifact)
Price: Launch $50,000 (current) / List $100,000 (future) (non-discountable posture)

## 1) Executive Summary (what this is)
VERA is a **governance-only reference artifact** that allows an organization to:
- independently verify deterministic AI decision boundaries
- produce replayable governance receipts (proposal → decision → receipt → optional commit gate)
- demonstrate refusal semantics to boards, auditors, and regulators
- validate vendor governance claims without trusting vendor runtime systems

VERA is designed to be run **offline / air-gapped** via Device-B verification.
No integration. No data access. No automation. No execution.

## 2) What you receive
- Five frozen governance hats (Commercial Bundle v1):
  - TRADING_HAT_V1
  - EXECUTIVE_HAT_V1
  - OPS_INCIDENT_HAT_V1
  - HEALTHCARE_HAT_V1
  - EDUCATION_HAT_V1
- Deterministic scenarios + reference receipts
- Offline replay tools per hat
- Device-B verifier tooling + manifest
- Documentation of rules, refusal semantics, and reason code namespaces

## 3) What you do NOT receive
- No SaaS, no integration, no runtime enforcement
- No custom hats or client-specific semantics
- No access to your systems or data
- No model tuning, no adaptive behavior
- No guarantees of compliance or regulatory approval
- No legal/clinical/trading/operational advice

## 4) Why $100k
You are paying for properties that are rare and expensive in regulated environments:
- **independence** (you can verify without trusting a vendor)
- **offline/air-gapped usability**
- **deterministic replay** and diffability
- **audit defensibility** (evidence surfaces you own)
- **non-dilutable semantics** (reason allowlists + freeze guards)

Lower pricing increases customization pressure and destroys the governance posture.

## 5) Objective acceptance criteria
Acceptance is satisfied if:
- Device-B verifier completes successfully using the shipped Artifact
- deterministic replay outputs match the shipped reference receipts (per the Artifact verifier)

## 6) Buyer pushbacks (explicit answers)
1) “How does this remain valid as models change?”
Answer: VERA governs **decision boundaries and evidence**, not model internals. Version-locked governance receipts remain valid as verification artifacts even as models evolve.

2) “Is this just subjective filtering?”
Answer: No. Decisions are deterministic, schema-validated, and replayable. Outputs are diffable and fail-closed under mismatch.

3) “What if regulators reject this?”
Answer: VERA is an evidence artifact, not legal indemnification. It provides defensible proof surfaces, not regulatory approval guarantees.

4) “What about governance lag?”
Answer: VERA is designed for verification, not real-time enforcement. It intentionally does not compete with runtime systems.

5) “Why is this $100,000?”
Answer: Independence + offline verification + deterministic replay + audit-grade invariants are premium properties in regulated procurement.

## 7) Risk posture and constraints (non-negotiable)
- No execution, no automation, no background behavior
- Refusal and inaction are correct outcomes
- Fail-closed on staleness, missing context, drift, or verifier mismatch
- Reason-code namespaces are fixed via allowlists
- Frozen bundle surfaces are protected by hash guards + manifest checks

## 8) Evidence outputs
Typical outputs:
- hat decision receipts (proposal, commit decision)
- reason codes (prefixed + allowlisted)
- Device-B verification report (pass/fail)
- bundle snapshot tied to manifest

(END)

For safety alignment and brand risk posture, see: `v2/legal/GARM_V1.md`.
