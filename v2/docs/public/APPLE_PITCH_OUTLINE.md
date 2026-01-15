# VERA v2 — Apple Pitch Outline (Public, Neutral)

## Positioning (no criticism)
This is a reference artifact showing deterministic execution governance:
- proposal vs commit separation
- drift gates
- stable refusal codes
- audit-safe ledger output
- domain modularity via hats

The question for Apple is not “can Siri be smarter?”
It’s: **why isn’t there a native governance surface for action?**

## The developer pressure point
If you give iOS/macOS developers a native way to:
- require explicit commit for risky actions
- surface conflicts at commit time
- emit stable reason codes
- log audit events deterministically

…they can build safer assistants and workflows with fewer trust failures.

VERA demonstrates the minimal semantics needed to make that possible.

## What Apple engineers can evaluate quickly
- Run `v2/demo/scripts/run_all_demos.sh`
- Observe deterministic outputs across runs
- Observe REQUIRE_RECOMMIT when proposal drift occurs
- Observe REFUSE when context is missing/stale or caps exceeded
- Observe “Coat” turning reasons into stable human messages (snapshot tests)

## Neutral gap map (Month 12 framing)
See: `v2/docs/public/APPLE_GAP_MAP_MONTH12.md`

Core gaps:
1) proposal vs commit separation
2) stable refusal codes
3) drift detection at commit time
4) audit-safe ledger output
5) domain modularity without precedence trees

## What we are NOT asking Apple for
- not a new model
- not autonomy
- not a “magic” UX layer
- not replacing App Intents

We are pointing to an execution-governance layer that can sit between:
- intent parsing
- app intents
- action execution

## Why this fits Apple’s values
- privacy-compatible (governance is local and deterministic)
- user consent is explicit
- safety is enforceable
- developer experience is clearer than ad-hoc prompting

## Call to action (low-friction)
1) Evaluate the artifact as an internal reference
2) Identify where a native governance surface could live
3) Decide whether to build, partner, or acquire
