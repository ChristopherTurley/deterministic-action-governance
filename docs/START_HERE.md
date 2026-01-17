# START HERE — VERA Deterministic Governance (90 seconds)

VERA is a **governance-only reference artifact** that demonstrates a missing primitive in modern AI systems:

**Proposal → deterministic decision → auditable receipt → (optional) operator commit**

This repo does **not** automate anything and does **not** execute side effects.
Its purpose is to prove that:
- refusal/inaction are first-class outcomes
- decisions are deterministic (re-runable and diffable)
- every decision produces an auditable receipt surface

If you only do one thing: run the invariants.

---

## 1) Run the invariant suite (must be green)

```bash
python3 -m pytest -q

