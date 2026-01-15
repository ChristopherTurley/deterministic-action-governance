# Embedding Examples (Conceptual) — Month 14.2

This document shows how VERA can be embedded into different host systems
without changing their execution model, permissions, or UI.

These are **conceptual integrations**, not SDKs or implementations.

---

## Principles shared by all examples

- VERA receives proposals, not commands
- VERA returns decisions, not actions
- Execution remains entirely with the host
- Permissions and consent remain native
- Removing VERA does not break the host system

---

## Example 1 — Local CLI Tool

### Host context
A command-line tool that performs local file operations.

### Integration pattern
1) User issues a CLI command
2) Host submits a proposal to VERA describing the intended action
3) VERA returns a decision
4) If ALLOW_FOR_COMMIT, host asks user for explicit commit
5) Host executes the command after commit

### What VERA adds
- Explicit proposal/commit separation
- Refusal and failure semantics
- Audit trail for sensitive operations

### What VERA does not change
- CLI syntax
- File permissions
- Execution environment

---

## Example 2 — Local Desktop Application

### Host context
A desktop app that performs user-initiated tasks.

### Integration pattern
1) User initiates an action via existing UI
2) Host submits a proposal to VERA
3) VERA returns a decision
4) UI requests explicit confirmation if required
5) Host executes using existing logic

### What VERA adds
- Deterministic governance before execution
- Clear refusal reasons
- Visibility into decision history

### What VERA does not change
- UI layout or flows
- App permissions
- Execution timing

---

## Example 3 — Service Wrapper (Internal)

### Host context
An internal service that mediates access to sensitive operations.

### Integration pattern
1) Upstream service submits a proposal
2) VERA evaluates and returns a decision
3) Explicit commit required from authorized operator
4) Service executes after commit

### What VERA adds
- Separation of intent from authority
- Auditable commit records
- Clear denial vs failure semantics

### What VERA does not change
- Authentication system
- Service APIs
- Retry or scheduling logic

---

## Example 4 — Automation System (Non-Autonomous)

### Host context
A system that supports user-triggered automation but avoids autonomy.

### Integration pattern
1) User defines an automation trigger
2) Each run submits a fresh proposal to VERA
3) VERA evaluates context and returns a decision
4) Explicit commit required per run (or per defined boundary)
5) Host executes if committed

### What VERA adds
- Guardrails against silent autonomy
- Fresh authority per execution
- Deterministic refusal when context is stale

### What VERA does not change
- Trigger mechanisms
- Scheduling engine
- Execution runtime

---

## Why these examples matter

Across all examples:
- VERA is removable
- VERA does not own execution
- VERA does not own permissions
- VERA does not optimize for success paths
- VERA optimizes for safety and clarity

---

## Anti-patterns (what not to build)

- Auto-executing on ALLOW_FOR_COMMIT
- Caching commits for reuse
- Treating ledger access as control
- Hiding refusals to “improve UX”

These violate the integration contract.

---

Status: Month 14 — Embedding Examples (Conceptual)  
Change policy: clarification-only changes allowed; no power expansion without invariant revision  
Review expectation: written to survive adversarial review
