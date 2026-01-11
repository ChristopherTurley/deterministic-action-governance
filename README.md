Deterministic Action Governance
Execution Safety Semantics for AI-Assisted Systems

Overview
This repository documents a deterministic action governance model for AI-assisted systems that are capable of executing actions.
The material focuses exclusively on how actions are authorized, validated, refused, and audited.
It does not address intelligence quality, user experience design, or product strategy.
The goal is to make execution behavior explicit, inspectable, and failure-safe.

What This Repository Contains
A formal action contract defining execution semantics
A deterministic lifecycle separating proposal, commitment, execution, and refusal
A reproducible demonstration of governed behavior
A concrete failure scenario illustrating why these semantics matter
A neutral comparison describing what current frameworks cannot express safely
All content reflects completed work.
No roadmap or future capabilities are implied.

Core Guarantees
This model guarantees that:
Suggestions do not execute implicitly
Execution requires explicit, attributable authority
Authorization is contextual, not permanent
Conflicts are surfaced before execution
Refusal is a valid and correct system outcome
All externally meaningful actions are traceable
The system prefers doing nothing over acting under unclear authority.

What This Is Not
This repository is not:
A consumer product
An AI assistant or agent
An automation platform
A user interface design
A recommendation system
A business proposal
It introduces no autonomy and makes no claims about intelligence.

Intended Audience
This material is written for:
Platform and systems engineers
Security and trust teams
Product managers responsible for execution-level behavior
Technical leadership evaluating execution safety primitives
It is not written for marketing or end-user consumption.

Repository Structure
spec/
Formal action governance contract
demo/
Deterministic execution harness and outputs
docs/
Failure demonstration, system framing, and comparative analysis
Each document is self-contained and can be read independently.

Guiding Principle
A system that cannot explain why it acted should not act.

Status
This repository documents completed work.
It exists to be read, evaluated, and reasoned about.
Nothing further is implied by its publication.