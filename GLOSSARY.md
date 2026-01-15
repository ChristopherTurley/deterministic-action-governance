# Glossary

This glossary standardizes terminology used across the repository.
Terms are intentionally narrow to prevent semantic drift.

---

## Core lifecycle terms

### Proposal
An untrusted request or candidate action description.
A proposal is not authority.

Properties:
- may be incomplete or ambiguous
- may be rejected or refused
- must not execute anything by itself

### Decision
A deterministic classification of a proposal.
Examples:
- refuse
- fail
- unavailable
- allow-for-commit

A decision must be recordable without requiring UI interpretation.

### Commit
An explicit, attributable, synchronous operator authorization that allows execution.
A commit is the only mechanism that can transition from decision to execution.

Constraints:
- commits cannot be inferred
- commits cannot be delegated to the system
- commits do not grant permanent authorization

### Execution
A side effect or externally meaningful action.
Execution must never occur without a valid commit.

### Receipt
An auditable record of what the system decided and what happened.
Receipts are required for accountability.

---

## Outcome terms

### Refusal
A deliberate, correct "no" based on invariants, scope, safety, authority, or context TTL.
Refusals are first-class outcomes and not errors.

### Denial
A refusal due to missing permission or missing authority.
In this repo, denials are typically represented as refusal outcomes with authority-related reason codes.

### Failure
A breakdown in expected operation.
Failures must fail closed and must not trigger retries or automatic recovery.

### Unavailability
A capability is not present, not configured, or not reachable.
Unavailability is not a policy decision.

---

## Governance terms

### Invariant
A non-negotiable constraint that defines what the system will not do.
Breaking an invariant invalidates the model.

### Reason code
A stable identifier for why a refusal or constraint triggered.
Reason codes are designed to survive changes in wording.

### Ledger
An append-only record of proposals, decisions, commits, and outcomes.
The ledger is the canonical audit artifact.

### Drift
Any mismatch between:
- what the system claims
- what it actually does
- what was authorized

Drift must be surfaced explicitly.

### Context TTL
A time-to-live boundary that prevents stale context from being reused to justify action.
If TTL is exceeded or missing, the system must refuse or fail closed.

---

## Composition terms

### Hat
A domain governance lens that applies domain-specific constraints without changing core engine semantics.
A hat adds rules and classifications, not power.

### Coat
A presentation layer that maps stable reasons and outcomes to human-readable messages.
A coat may improve legibility, but must not change meaning.

---

## Design principles

### Fail closed
If the system cannot decide safely, it does nothing.
No best-effort side effects.

### Prefer refusal over unsafe action
Ambiguity is resolved by refusal or failure, not execution.

### No implicit authority
Consent and authority are explicit.
The platform remains the source of truth for identity and permissions.
