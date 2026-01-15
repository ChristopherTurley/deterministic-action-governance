# Deterministic Action Governance

A deterministic, fail-closed governance layer for AI-assisted systems that execute actions.  
**It separates proposal → decision → explicit commit** and produces auditable outcomes **without autonomy**.

[Start here: Evaluation Path](EVALUATE.md) • [Glossary](GLOSSARY.md) • [Docs Index](docs/INDEX.md)

## Guarantees
- Suggestions do not execute implicitly
- Execution requires explicit, attributable authority
- Authorization is contextual (not permanent)
- Conflicts are surfaced before execution
- Refusal is a valid, correct system outcome
- Externally meaningful actions are traceable
- The system prefers doing nothing over acting under unclear authority

## Non-goals
- Not an agent / not autonomous
- Not a consumer product
- Not an automation platform
- Not a UI design repository
- Not a permissions broker

## Trust anchors
- Invariants (constitution): `docs/invariants.md`
- Refusal taxonomy: `docs/refusal_model.md`
- Failure narratives: `docs/failure_modes.md`
- Threat model: `docs/threat_model.md`

Guiding principle: **A system that cannot explain why it acted should not act.**
## Public deposit lineage
This repository contains an earlier published “public deposit” artifact set under:
- `vera_v2_public_deposit/`

That folder is retained as a historical reference package. The current recommended reading path is:
- `EVALUATE.md`
- `GLOSSARY.md`
- `docs/INDEX.md`
