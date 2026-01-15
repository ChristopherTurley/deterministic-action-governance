# Security Review (Internal Simulation)

## Intended audience
Security reviewers evaluating containment, consent alignment, and drift resistance.

## Review stance (assumptions)
- Assume adversarial inputs
- Assume model hallucination
- Assume developer misuse
- Assume future pressure to “make it smoother”
- Treat vague guarantees as non-answers

## Objections (harsh)
1. “This is an agent in disguise.”
2. “Nothing stops silent escalation in later versions.”
3. “This could bypass platform consent models.”
4. “Prompt injection will cause execution drift.”
5. “Developers will abuse this to auto-execute.”
6. “Users won’t know who is in control.”
7. “Logs can leak sensitive information.”
8. “This becomes shadow policy enforcement.”
9. “Why not just use platform intent frameworks?”
10. “This pattern could spread badly and create ecosystem risk.”

## Response principles (how answers must be framed)
- Prove impossibility, not intent
- Prefer architectural constraints over promises
- Treat ambiguity as a refusal condition
- Keep “proposal vs commit” boundary explicit
- Keep “consent is downstream” explicit

## Non-negotiable containments
- No autonomy
- No background execution
- No implicit authority
- No permission brokering
- Fail closed

## Residual risks (acknowledged)
- External integrations can still be built unsafely outside VERA
- Miscommunication risk exists without careful language
- Logs require disciplined minimization by integrators

## Evidence of containment (what reviewers should verify)
- Invariants are explicit and testable
- Refusal taxonomy is exhaustive and deterministic
- Failure modes are distinguished from refusals
- No execution path exists without explicit commit

---
Status: Month 11 — Semantic Hardening  
Change policy: clarification-only changes allowed; no power expansion without invariant revision  
Review expectation: written to survive adversarial review
