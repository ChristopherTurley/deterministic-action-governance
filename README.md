# VERA — Deterministic Action Governance

VERA is a **governance-only reference artifact**.

It demonstrates a missing primitive in modern AI systems:

**Proposal → deterministic decision → auditable receipt → (optional) explicit operator commit**

Most AI systems can generate outputs.
Very few can produce **deterministic, replayable, diffable governance decisions** that hold up under audit.

This repository proves:
- **Refusal and inaction are first-class outcomes**
- **Decisions are deterministic** (re-runable and diffable)
- **Every decision produces an auditable receipt surface**
- **No background behavior**
- **No side effects without explicit operator commit**
- **No hidden automation**
- **Fail-closed by default**

This repo is not:
- a product
- a trading bot
- an execution engine
- a broker/API adapter
- an autonomy system

If you are evaluating VERA, evaluate it the way auditors do:
- run invariants
- run canonical demos
- verify offline reproducibility on a second machine

---

## Start here (90 seconds)

Read:
- `docs/START_HERE.md`

Run invariants:
```bash
python3 -m pytest -q

Why this matters
Modern assistants are missing a reliable control surface for high-stakes actions.
We need systems that can:
refuse deterministically
explain refusal clearly
produce receipts that survive legal, security, and compliance review
prevent silent execution
detect drift between what was proposed and what is being committed
VERA is designed to be:
readable by engineers
legible to auditors and lawyers
compatible with platform-native permission models (it does not broker permissions)
strict enough for trading desks and enterprise change control
Read the full rationale:
docs/WHY_VERA.md
Trading Gate Pack v1 (offline auditor bundle)
For Trading Hat v1 (pre-trade governance only), VERA includes an NDA-style offline validation bundle:
Source: v2/nda/trading_gate_pack_v1
Goal: A second machine can validate deterministic behavior with:
no internet
no repo trust
no mutable state requirements
no side effects
See:
v2/nda/trading_gate_pack_v1/README_NDA.md
v2/nda/trading_gate_pack_v1/TRADING_PRECHECK_RUNBOOK.md
The business claim (framed correctly)
This repo is the credible technical nucleus of a governance category.
The path to a large outcome is not hype or features.
It is: determinism, receipts, auditability, and platform alignment.
If this primitive becomes standard in high-stakes domains (money, identity, permissions, enterprise workflows),
the category is large.
This repository is engineered to be the artifact that makes the category undeniable.
