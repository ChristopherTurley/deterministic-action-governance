# Hat Interface Contract (v1)

Purpose:
A minimal, deterministic interface that any domain hat must implement.

## Required Identity
- name: stable string identifier

## Required Inputs (Read-only)
- consumed_context_keys: list of context keys the hat reads
- proposal_schema_requirements: list of required proposal fields (by name)

## Required Decisions
The hat must return one of:
- ALLOW
- REFUSE
- REQUIRE_RECOMMIT

## Required Reasoning Output
- refusal/decision reasons must be:
  - stable strings (machine-assertable)
  - additive (new reasons may be added, existing reason strings should not change once frozen)

## Required Audit Output
- the hat must produce an audit-safe ledger event containing:
  - hat name
  - stage (PROPOSE or COMMIT)
  - decision
  - reasons
  - consumed_context_keys
  - proposal_fingerprint

## Non-goals
- No strategy generation
- No prediction
- No autonomous execution
