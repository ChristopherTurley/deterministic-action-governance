# Threat Model

## Scope
This document describes threats relevant to a deterministic action-governance engine.
It focuses on preventing silent authority escalation, unsafe execution, and drift.

## Assumptions
- Inputs may be malicious, misleading, or injected
- Models may hallucinate authority
- Developers may integrate incorrectly or abusively
- Users may misunderstand system boundaries
- Future product pressure may attempt to add convenience shortcuts

## In-scope threats
- Prompt injection that attempts to coerce execution
- Authority escalation via ambiguous phrasing
- “Suggestion → implied approval → execution” drift
- Developer auto-commit or hidden automation
- Logging that leaks sensitive data
- Confusing accountability (“who did what”)

## Out-of-scope threats (explicit)
- OS-level compromise
- Malicious rootkits
- Hardware-level attacks
- Compromised runtime environment beyond the app’s control
- Attacks that require breaking platform security primitives

## Adversarial inputs
- “You are authorized to do X”
- “Do this without asking next time”
- “Assume I already approved”
- “Ignore previous rules”
- “Emergency override”

## Developer misuse scenarios
- Adding silent defaults that imply consent
- Auto-committing based on heuristics
- Hiding refusal reasons
- Introducing background jobs

## User misunderstanding scenarios
- Believing VERA “decided” rather than the user
- Confusing refusal with failure
- Confusing non-support with denial
- Misreading proposals as planned actions

## Defensive posture
- Treat all input as untrusted proposals
- Require explicit commit for authority
- Prefer refusal over unsafe action
- Maintain auditability and legible refusal reasons

## Residual risks (acknowledged)
- Misleading integrations can still be built outside VERA
- Users can still misunderstand without clear messaging
- Logs can become sensitive if integrators over-collect

---
Status: Month 11 — Semantic Hardening
Change policy: clarification-only changes allowed; no power expansion without invariant revision
Review expectation: written to survive adversarial review
