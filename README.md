# VERA — Deterministic Action Governance

This repository is a **governance-only reference artifact**.

It is:
- safe to clone
- safe to audit
- safe to demo

It is **not**:
- a product
- an automation system
- an execution adapter

Key guarantees:
- **No background behavior**
- **No side effects without explicit operator commit**
- **Refusal and inaction are correct outcomes**
- **Determinism is enforced via tests**

## Evaluate in 90 seconds

1) Read the canonical evaluator path:
- `docs/START_HERE.md`

2) Run the invariants:
- `pytest -q`

3) Run the canonical demos:
- see `v2/docs/demo_index.md`
