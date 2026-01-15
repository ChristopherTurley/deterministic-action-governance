# Deterministic Action Governance

A deterministic, fail-closed governance layer for AI-assisted systems that are capable of executing actions.

This repository documents **how execution is authorized, refused, and audited** — not how intelligence is produced.

The core guarantee is simple:

> **No externally meaningful action occurs without explicit, attributable human authority.**

---

## What this is

This project defines and demonstrates a **deterministic execution governance model** that:

- Treats all model output as **untrusted proposals**
- Separates **proposal → decision → explicit commit**
- Prefers refusal over unsafe or ambiguous execution
- Produces auditable, reproducible outcomes
- Makes failure visible and non-destructive

The system is intentionally **fail-closed**.  
If authority, context, or intent is unclear, **nothing happens**.

---

## What this is not

This repository is explicitly **not**:

- An autonomous agent
- A consumer assistant
- An automation platform
- A UI or interaction design project
- A permissions broker
- A recommendation or strategy system

It introduces **no autonomy** and makes **no claims about intelligence quality**.

---

## Start here

For a structured evaluation path:

- **`docs/START_HERE.md`** — recommended entry point
- **`EVALUATE.md`** — how to assess this repository quickly
- **`GLOSSARY.md`** — precise terminology
- **`docs/INDEX.md`** — full documentation map

These documents are written to respect limited review time.

---

## Deterministic demos

The repository includes reproducible demos that exercise the governance model end-to-end:

```bash
./v2/demo/scripts/run_all_demos.sh
python3 run_vera_v2.py
