# Hat Reason Codes Registry v1

Status: Locked (Hats v1)
Scope: Documentation-only registry
Change policy: additive only with explicit Hat revision

---

## Purpose

This document is the **canonical registry** for all Hat-scoped invariant reason codes.

It exists to ensure:
- determinism across domains
- audit consistency
- zero ambiguity during review
- prevention of silent power expansion

All Hat-level invariants **must** reference a reason code defined here.

---

## Design rules (non-negotiable)

1. Reason codes are **stable identifiers**
2. Reason codes are **namespaced by domain**
3. Reason codes map to **existing refusal categories**
4. Reason codes **do not introduce new logic**
5. Adding a reason code requires a Hat revision

---

## Relationship to core refusal taxonomy

- Core refusal categories remain unchanged:
  - AUTHORITY
  - SCOPE
  - SAFETY
  - INVARIANT
  - CONTEXT_TTL

- Hat reason codes always use:
  - `category = INVARIANT`
  - `reason_code = INV_<DOMAIN>_<DESCRIPTION>`

---

# Trading Hat (INV_TRADING_*)

- INV_TRADING_MISSING_REQUIRED_FIELD  
  Required trade fields not provided.

- INV_TRADING_MAX_LOSS_PER_TRADE_EXCEEDED  
  Proposed trade exceeds declared per-trade loss limit.

- INV_TRADING_MAX_DAILY_LOSS_EXCEEDED  
  Proposed trade exceeds remaining daily loss capacity.

- INV_TRADING_MAX_TRADES_PER_DAY_EXCEEDED  
  Proposed trade exceeds declared daily trade limit.

- INV_TRADING_INSTRUMENT_NOT_ALLOWED  
  Instrument not permitted by trader declaration.

- INV_TRADING_OUTSIDE_TIME_WINDOW  
  Trade proposed outside allowed trading hours.

- INV_TRADING_OVERRIDE_REQUIRES_COMMIT  
  Rule override attempted without explicit commit.

---

# Ops / Incident Response Hat (INV_OPS_*)

- INV_OPS_REQUIRES_EXPLICIT_COMMIT  
  High-risk operational action requires explicit authority.

- INV_OPS_PRODUCTION_SCOPE_REQUIRES_CONFIRM  
  Production-impacting changes require explicit confirmation.

- INV_OPS_NO_BACKGROUND_RETRY  
  Background retries or automatic recovery are not allowed.

- INV_OPS_MISSING_CHANGE_SUMMARY  
  Operational proposal missing required change context.

---

# Platform Assistants Lens (INV_PLATFORM_*)

- INV_PLATFORM_NO_PERMISSION_BROKERING  
  Hat must not broker or infer platform permissions.

- INV_PLATFORM_NO_BACKGROUND_BEHAVIOR  
  Hat must not introduce background execution.

---

# Education Hat (INV_EDU_*)

- INV_EDU_NO_GRADING  
  Grading or evaluation behavior is not allowed.

- INV_EDU_NO_SURVEILLANCE  
  Monitoring or profiling learners is forbidden.

- INV_EDU_INTEGRITY_BOUNDARY_VIOLATION  
  Proposal violates declared learning integrity constraints.

- INV_EDU_MISSING_CONTEXT  
  Required educational context not provided.

---

# Healthcare Hat (INV_HEALTH_*)

- INV_HEALTH_NO_DIAGNOSIS  
  Diagnostic behavior is forbidden.

- INV_HEALTH_NO_TREATMENT_RECOMMENDATION  
  Treatment recommendation is forbidden.

- INV_HEALTH_CLINICIAN_AUTHORITY_REQUIRED  
  Explicit clinician authority is required.

- INV_HEALTH_MISSING_REQUIRED_CONTEXT  
  Required clinical context not provided.

---

# Competitive Sports Hat (INV_SPORTS_*)

- INV_SPORTS_NO_OPTIMIZATION  
  Strategy optimization is not allowed.

- INV_SPORTS_AUTHORITY_REQUIRED  
  Explicit authority required for competitive decisions.

- INV_SPORTS_MISSING_CONTEXT  
  Required game context not provided.

---

# Executive Hat (INV_EXEC_*)

- INV_EXEC_ROLE_AUTHORITY_REQUIRED  
  Decision requires appropriate executive authority.

- INV_EXEC_NO_ADVICE  
  Advisory or recommendation behavior is forbidden.

- INV_EXEC_MISSING_CONTEXT  
  Required decision context not provided.

---

# High-Focus Worker Hat (INV_FOCUS_*)

- INV_FOCUS_NO_NUDGING  
  Nudging or behavioral manipulation is forbidden.

- INV_FOCUS_CONSTRAINT_VIOLATION  
  Proposal violates declared focus constraints.

- INV_FOCUS_MISSING_CONTEXT  
  Required focus context not provided.

---

# Designer Hat (INV_DESIGN_*)

- INV_DESIGN_NO_OPTIMIZATION  
  Aesthetic or creative optimization is forbidden.

- INV_DESIGN_BOUNDARY_VIOLATION  
  Proposal violates declared creative boundaries.

- INV_DESIGN_MISSING_CONTEXT  
  Required design context not provided.

---

# Engineer Hat (INV_ENG_*)

- INV_ENG_AUTHORITY_REQUIRED  
  Explicit authority required for engineering changes.

- INV_ENG_NO_ENFORCEMENT  
  Hat must not enforce execution or CI/CD behavior.

- INV_ENG_MISSING_CONTEXT  
  Required engineering context not provided.

---

## Review guidance

A reviewer should confirm:
- All Hat invariants reference this registry
- No Hat introduces undocumented reason codes
- Removing all Hats leaves core behavior unchanged

---

Status: Hats v1 — Reason Codes Registry (Locked)  
Review expectation: survives adversarial platform, legal, and security review
