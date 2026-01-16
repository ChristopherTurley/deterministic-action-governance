# Platform Gap Note: Deterministic Execution Boundaries

Status: Reference note (non-prescriptive)  
Scope: Execution governance patterns for AI-mediated actions  
This repository is a non-autonomous, non-background, evaluator-safe reference artifact.

## Terms

- Decision: intent resolution, recommendation, classification, routing, planning.
- Execution: any irreversible side effect (device state change, network call, filesystem mutation, user data change).

A deterministic execution boundary is a system-enforced separation where:
- Decisions may occur freely.
- Execution is permitted only via an explicit, human-attributed commit.
- Replays are mechanically blocked.
- Outcomes are audit-legible.
- Inaction is a valid terminal outcome.

This note describes an observable absence of a first-class execution boundary primitive in common AI-to-action stacks.

## Observed Pattern

In many tool/intent systems, execution is reached through a handler path that combines:
- decision logic
- permission prompting
- the side effect itself

This coupling makes it difficult to guarantee, in a testable way, that:
- an explicit operator commit occurred immediately prior to execution
- a side effect is single-shot (at-most-once) across retries/replays
- revocation can prevent a pending action before the side effect
- refusal/inaction are terminal outcomes with invariant semantics
- execution can be audited via tamper-evident receipts rather than informal logs

## What This Repo Demonstrates

This repository demonstrates (without performing real-world side effects by default) that an execution boundary can be expressed as test-enforced mechanics:

- Explicit commit gate
  - decision produces a PROPOSE artifact
  - execution requires an explicit commit artifact
- Single-shot enforcement
  - at-most-once semantics keyed to decision checksum and commit nonce
- Allowlist execution
  - executors must be registered and explicitly enabled
  - revocation disables immediately
- Receipt chain
  - pre-execution authorization receipt
  - executor-specific receipt
  - post-result receipt
  - receipts are tamper-evident (checksummed)
- No background behavior
  - denylisted background primitives are absent by construction and test

The repo is intentionally constrained:
- no background scheduling
- no autonomous retries
- no agent loops
- no hidden authority
- inaction is success

## How To Evaluate (No Demos)

Run:

python3 -m pytest

All claims above are intended to be enforced by tests.

## Non-Goals

This note does not propose APIs, entitlements, or integrations.
It is a reference description of an execution-governance boundary as a testable primitive.
