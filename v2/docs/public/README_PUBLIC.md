# VERA v2 — Deterministic Action Governance (Public Reference)

This is a reference artifact demonstrating deterministic action governance:

- proposals are non-binding
- commits are explicit
- conflicts are surfaced, never hidden
- outcomes are ALLOW / REFUSE / REQUIRE_RECOMMIT
- decisions are logged with stable reason codes

This is not autonomy.
This is execution safety.

## What this proves

1) Determinism
Same inputs produce the same outputs.

2) Fail-closed defaults
Missing context, stale context, missing fields, unknown hats -> REFUSE.

3) Commit gates
Proposal drift at commit time -> REQUIRE_RECOMMIT.

4) Auditability
Each decision emits a ledger event with:
- stage (PROPOSE / COMMIT)
- decision (ALLOW / REFUSE / REQUIRE_RECOMMIT)
- reasons (stable strings)
- proposal fingerprint
- consumed context keys

## What this intentionally does not do

- No trading strategy, prediction, or signals
- No background memory
- No autonomous execution
- No implicit domain routing

## One-command verification

From repo root:
v2/demo/scripts/run_all_demos.sh
