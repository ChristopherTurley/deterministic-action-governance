# VERA v2 — One Pager (Public)

## Problem
Most assistants optimize for fluency, not execution safety.
When they act, it is often:
- unclear what was proposed vs executed
- unclear why something was allowed or refused
- non-deterministic across runs
- difficult to audit

## Solution
A deterministic governance layer that enforces:
- proposal-first (non-binding)
- explicit commit gates
- fail-closed defaults
- stable refusal codes
- audit-safe ledger output

## Primitives
- PROPOSE: validate inputs, decide ALLOW or REFUSE
- COMMIT: detect drift, decide ALLOW / REQUIRE_RECOMMIT / REFUSE
- LEDGER: log decision + reasons + fingerprints

## Demonstrated domains (Hats)
- Trading Hat v1: mechanical constraints only, no strategy
- Focus Hat v1: caps + drift gating, no “motivation engine”

## Claim
Execution Intelligence can exist without autonomy.
