Deterministic Action Governance
Action Contract v1.1

Purpose

This document defines a deterministic governance contract for AI-assisted
systems that are capable of executing actions.

It specifies how actions are proposed, authorized, executed, refused, and
audited. It does not define intelligence, reasoning quality, or user
interaction.


Core Principle

Suggestions are not actions.

Any system that collapses suggestion and execution into a single step
eliminates clear responsibility, obscures causality, and fails unpredictably
under ambiguity.

This contract enforces an explicit boundary between proposal, commitment,
and execution.


Action Lifecycle

All actions progress through the following lifecycle:

INTAKE
→ PROPOSED
→ (COMMITTED | REFUSED)
→ (EXECUTED | ABORTED)
→ LEDGERED


Intake

Raw user or system input is received.
No side effects are permitted at this stage.


Proposed

One or more inert action proposals are generated.
Proposals may include metadata but carry no execution authority.


Committed

Commitment represents an explicit transfer of execution authority.

A commitment must be attributable to a declared authority source and recorded
as a first-class event.


Refused

Refusal is a valid terminal outcome.
Refusals must be explicit, deterministic, and ledgered.


Executed / Aborted

Execution may occur only after commitment.
Silent execution is forbidden.


Ledgered

All terminal outcomes must be recorded in an append-only ledger.
Ledger entries preserve causal order.


Authority Sources

Commitment may be issued by:

- Operator authority (explicit human action)
- Policy authority (pre-authorized, operator-defined rule)

All authority sources must be explicit, inspectable, revocable, and ledgered.

Absence of valid authority must result in refusal.


Determinism

Determinism is guaranteed over declared inputs, not global world state.

Declared inputs include:
- Raw intake
- Context snapshot identifier
- Active policy set
- Execution mode identifier

Identical declared inputs must produce identical proposals and gating behavior.

Dependencies that cannot be captured must be treated as non-binding and fail
closed or require operator authority.


Conflict Detection

Each proposal must declare:
- Resources it intends to mutate
- Temporal constraints
- Exclusive preconditions

Conflict detection is bounded to overlapping declared claims.

If conflict analysis exceeds bounded limits, the system must refuse and ledger
the refusal.

Silent conflict resolution is forbidden.


Refusal Semantics

Refusal is a correctness outcome.

The system must refuse when:
- Authority is missing or invalid
- Preconditions are unmet
- Conflicts are unresolved
- Verification artifacts are absent


Verification Requirements

Action classes may declare required verification artifacts.

If required artifacts are missing:
- Policy authority may not override
- Operator authority may override only with explicit acknowledgment

Artifact presence or absence must be ledgered.


Ledger Scope

The ledger records contract-level events only:
- Proposal creation
- Commitment
- Refusal
- Conflict outcomes
- Execution or abortion

Internal reasoning and planning are out of scope.

Execution without a valid commitment artifact is non-compliant.


Scope Clarification

This contract governs externally meaningful state transitions only.

It does not govern:
- Internal reasoning
- Model sampling
- UI rendering
- Intermediate computation


Minimal Claim

A system that cannot explain why it acted should not act.
