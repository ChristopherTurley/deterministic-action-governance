What Current AI Action Frameworks Cannot Express Safely

This document describes limitations in how most AI action frameworks express
execution authority.

It does not critique specific platforms or implementations.


Observation

Most frameworks collapse suggestion and execution into a single step.

This makes it difficult to represent:
- Expiring authority
- Context-dependent validity
- Refusal as a correct system outcome


Consequences

- Responsibility becomes diffuse
- Conflicts resolve implicitly
- Auditability is reconstructed after execution


Alternative Model

A governance-first model makes the following first-class:
- Action proposals
- Explicit commitment
- Authority validation
- Deterministic refusal
- Causal ledgers

These semantics are difficult to express natively today.


Minimal Statement

If execution authority is implicit, responsibility cannot be explicit.
