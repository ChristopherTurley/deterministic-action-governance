Deterministic Action Governance
System-Level Framing

Problem

As AI systems are permitted to modify state and act asynchronously, the
boundary between suggestion and execution becomes operationally significant.

Most systems treat this boundary implicitly.


Definition

Deterministic action governance is a system-level substrate that:
- Separates proposal from execution
- Makes authority explicit
- Surfaces conflicts before execution
- Preserves causality through an append-only ledger
- Fails closed under uncertainty

It defines how intelligence is allowed to act, not intelligence itself.


Stack Placement

[Intelligence / Reasoning]
        ↓
[Action Proposals]
        ↓
[Deterministic Action Governance]
        ↓
[Execution APIs]


Failure Philosophy

Correct behavior includes refusal, inaction, and explicit surfacing of
conflicts.

The system optimizes for trust under failure, not speed under success.


Minimal Claim

AI systems that can act must expose how and why they are allowed to act.
