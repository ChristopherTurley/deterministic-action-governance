# VERA Commercial Bundle v1 — License (LOCKED)

Effective date: 2026-01-17
Applies to: VERA Commercial Bundle v1 (“Artifact”)
Bundle ID: COMMERCIAL_BUNDLE_V1

## 1) What you are receiving
You are receiving a **governance-only reference artifact** consisting of:
- documentation
- deterministic hat decision code (non-executing)
- deterministic scenarios and reference receipts
- offline replay and verification tools (Device-B)
- verification outputs you generate locally

The Artifact is designed to be run by the Customer in an offline or air-gapped environment.
The Artifact does not integrate with Customer systems and does not access Customer data.

## 2) License grant (evaluation + internal verification only)
Subject to the restrictions below, Customer is granted a non-exclusive, non-transferable right to:
- install and run the Artifact internally for governance verification and audit evidence generation
- generate, retain, and present verification outputs and receipts for internal governance, board, audit, and regulatory discussions

## 3) Restrictions (NON-NEGOTIABLE)
Customer may not, and may not permit others to:
- modify, adapt, or create derivative works of the hats, rules, reason codes, or verifier tooling
- request, require, or expect **custom hats**, **custom rules**, or **client-specific semantics**
- deploy the Artifact as a production system, runtime controller, or enforcement engine
- represent the Artifact as providing legal advice, clinical advice, trading advice, or operational advice
- use the Artifact to process or store Customer production data, PHI, or other regulated data
- remove or alter reason-code prefixes, token allowlists, or Device-B verification constraints
- repackage, resell, sublicense, or distribute the Artifact outside the Customer’s organization

No support obligation is implied or created by this license.

## 4) No warranties; evidence artifact only
THE ARTIFACT IS PROVIDED “AS IS”.
The Artifact is an evidence-generation and verification surface.
It is not a guarantee of compliance, regulatory acceptance, or legal defensibility in any specific jurisdiction.

## 5) Limitation of liability
To the maximum extent permitted by law:
- Vendor is not liable for indirect, incidental, special, consequential, exemplary, or punitive damages.
- Vendor’s total aggregate liability arising from the Artifact will not exceed the fees paid for the Artifact.

## 6) No reliance / no substitution
Customer acknowledges:
- The Artifact does not substitute for Customer’s own governance, controls, or legal review.
- Outputs are inputs to Customer’s governance process, not determinations of compliance.

## 7) Acceptance criteria (objective)
Acceptance is satisfied if:
- Device-B verifier completes successfully using the shipped Artifact
- deterministic replay outputs match the shipped reference receipts (within the Artifact’s defined verification process)

## 8) Audit evidence handling
Customer owns the outputs it generates and may present them to auditors/regulators as evidence of:
- deterministic decision boundary behavior
- refusal semantics
- replayability and invariance controls

## 9) Term
This license is effective upon payment and remains in effect for internal use,
subject to termination upon material breach of the Restrictions section.

(END)
---

## Evaluation License vs Commercial Governance Reference License

This artifact may be licensed under one of the following non-exclusive governance reference licenses.
Both licenses apply to the **same artifact**. No technical restrictions, feature gates, or execution controls
differentiate the licenses. Only **rights of reliance and representation** differ.

### A) Evaluation License (Non-Reliance)

Under the Evaluation License, the licensee may:

- Access, read, and internally circulate the artifact
- Review governance structure, refusal semantics, and documentation
- Use the artifact for internal education, assessment, and discussion
- Evaluate suitability for future governance or policy use

The licensee may **not**:

- Represent the artifact as an approved or adopted governance baseline
- Cite the artifact in formal policy, audit, or compliance materials
- Rely on the artifact as authoritative in regulatory, legal, or risk decisions
- Assert endorsement, certification, or approval by the licensor

There is **no expiration** of access. The limitation applies solely to rights of reliance.

---

### B) Commercial Governance Reference License (Reliance Granted)

Under the Commercial Governance Reference License, the licensee may:

- Exercise all Evaluation License rights
- Cite the artifact as a governance reference in internal documentation
- Rely on the artifact in governance, risk, and policy discussions
- Represent the artifact as an adopted governance reference
- Use the artifact as a non-executing baseline for audits, reviews, and design discussions

This license grants **permission to rely**, not permission to execute.

#### Formal reliance contexts (what this license enables)
Under this license, Customer may use and cite the Artifact in formal internal governance contexts, including:
- internal governance frameworks and control libraries
- executive, board, and risk committee materials
- audit preparation and evidence narratives
- regulatory / examiner discussions (as a reference artifact, not a compliance determination)
- internal policy and AI risk documentation

**The right of reliance above is the primary commercial value of this license.**


---

### Shared Constraints (Both Licenses)

Regardless of license type, the artifact:

- Performs no automation
- Executes no actions
- Integrates with no production systems
- Enforces no policies
- Moderates no content
- Makes no operational decisions

All outputs are explanatory, non-binding, and governance-only by design.

