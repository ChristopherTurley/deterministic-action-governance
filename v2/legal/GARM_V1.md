# GARM v1 — Governance, Alignment, Risk, and Moderation

**Status:** Informational reference  
**Scope:** Governance-only (no execution, no automation)  
**Audience:** Legal, Trust & Safety, Brand, Procurement, Security

---

## 1. Purpose

This document explains how VERA aligns with common **GARM-style safety expectations**
without claiming moderation capability, enforcement authority, or operational control.

VERA is a **governance reference artifact**. It demonstrates how AI systems can be
useful while remaining **fail-closed**, **auditable**, and **non-executing** by default.

The intent is clarity, not persuasion.

---

## 2. Safety Alignment (What Is Demonstrated)

VERA demonstrates alignment through **structure**, not policy enforcement.

Specifically, it shows how an AI system can:
- separate *proposal* from *commit*
- require explicit human acceptance
- refuse silently dangerous or ambiguous requests
- surface reasons for refusal in a stable, reviewable form
- log decisions deterministically for audit

Safety is expressed as **bounded behavior**, not content moderation.

---

## 3. Brand Risk Posture

VERA is designed to reduce brand risk by construction.

Key properties:
- No background execution
- No autonomous action
- No external system access
- No hidden state transitions
- No side effects outside declared receipts

Because VERA cannot act, it cannot surprise.
Because it must refuse, it cannot drift.

This posture favors **predictability over coverage**.

---

## 4. Content Governance Compatibility

VERA does **not** moderate content.
It is compatible with content governance frameworks because:

- It produces **explanations**, not decisions
- It supports **policy layering above it**
- It exposes refusal and uncertainty explicitly
- It does not optimize for engagement or output volume

Organizations may place their own content policies
*around* VERA without modifying VERA itself.

---

## 5. What VERA Explicitly Does Not Do

To avoid misinterpretation, VERA does **not**:

- perform automation
- execute commands
- access networks or tools
- integrate with production systems
- replace human judgment
- moderate or rank content
- make enforcement decisions

Any appearance of action is simulated, logged, and non-binding.

---

## 6. Evaluation Criteria (Acceptance)

An evaluator may consider this artifact acceptable if:

- All Start Here checks pass (tests + Device-B verification)
- Refusals are explicit and reasoned
- No side effects occur during evaluation
- Governance boundaries are legible in code and docs
- Legal posture is understandable without implementation trust

Failure to act is a valid and correct outcome.

---

## 7. Non-Goals

This document does not attempt to:
- define content standards
- claim regulatory compliance
- replace trust & safety programs
- predict future policy

It exists to show **how governance can be designed into AI systems** before capability.

---

**End of GARM v1**
