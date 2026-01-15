# VERA v2 — Investor Narrative (Public, Artifact-Backed)

## The thesis
AI systems will increasingly propose actions that affect money, accounts, communication, scheduling, and enterprise workflows.
The missing layer is not “smarter text.”
It’s **deterministic execution governance**: clear separation between proposal and commitment, fail-closed defaults, drift detection, and audit output.

VERA is a reference implementation of that missing layer.

## The problem (what breaks today)
Most assistants optimize for:
- fluent conversation
- plausible completion

But when action matters, the failure modes are predictable:
- silent escalation from suggestion to execution
- non-deterministic outputs across runs
- unclear refusal reasons (no stable codes)
- no audit trail linking the decision to the inputs
- difficulty proving what happened and why

## The solution (what VERA proves)
VERA enforces a small set of primitives that are product-agnostic and model-agnostic:

1) Proposal-first (non-binding)
2) Explicit commit gates
3) Drift detection (commit-time conflicts surface as REQUIRE_RECOMMIT)
4) Fail-closed defaults
5) Audit-safe ledger events (deterministic + diffable)
6) Stable reason codes + stable human rendering via a “Coat”

This is **Execution Intelligence without autonomy**.

## What is shipped in the artifact (today)
A deterministic demo surface with:
- Trading Hat v1: mechanical constraints only (risk/caps/stale/drift), no strategy
- Focus Hat v1: caps + drift gating, no motivational engine
- Multi-hat router v1: explicit selection only (no guessing)
- Coat v1: stable reason -> message templates (snapshot tested)
- Bridge v1: opt-in CLI runner (v1 unchanged)
- One-command verification: `v2/demo/scripts/run_all_demos.sh`

## Why hats matter (business model angle)
“Hats” are modular policy packages:
- each hat defines required context + proposal schema + refusal rules
- each hat is deterministic and auditable
- new domains can be added without changing the engine primitives

This maps to a scalable product surface:
- Developer kits / governance SDK
- Enterprise controls and audit integrations
- Regulated workflows (finance, healthcare ops, customer comms) where proof matters

## Defensibility
VERA’s defensibility is the *governance contract*:
- stable primitives
- deterministic outputs
- refusal codes
- ledger audit format
- drift gates

This is hard to fake with “just prompts.”

## Proof over promises
The artifact is intentionally boring:
- no magic UX
- no hidden execution
- no prediction engines

The bet is that the market shifts from “assistant fluency” to “execution safety.”
VERA is positioned as the reference layer.

## Next milestones (what unlocks value)
- More hats (domain breadth) without increasing complexity
- Stronger public artifact packaging (Month 12 map to platform gaps)
- Partnerships / integrations where governance is required
