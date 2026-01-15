# Month 12 — Apple API Gaps (Neutral Developer Framing)

This is a neutral description of what is often missing in assistant stacks.

## Gap 1: Proposal vs Commit separation
VERA enforces:
- Proposal (non-binding)
- Commit (explicit operator confirmation)
- Drift detection

## Gap 2: Stable refusal reasons
VERA emits stable reason codes and coat-rendered human output.

## Gap 3: Reversibility metadata
Policy blocks and dry runs still emit reversal fields (reversal_id, undo_hint).
See: v2/docs/side_effects_contract_v1.md

## Gap 4: Domain modularity without precedence trees
VERA uses:
- Hats (domain constraints)
- Router (explicit selection only)
No guessing. No nested policy DSL.

## Gap 5: Audit-safe ledger
Governance proofs require deterministic, diffable ledger output.
