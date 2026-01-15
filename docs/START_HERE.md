# Start Here

This document is the fastest way to understand **what this repository is**, **what problem it solves**, and **how to evaluate it** without reading everything.

If you only read one file, read this one.

---

## What problem this repository addresses

Modern AI systems are increasingly capable of producing **real-world effects**:
- executing commands
- modifying state
- triggering workflows
- interacting with external systems

The core risk is not intelligence — it is **execution ambiguity**.

Specifically:
- When does a suggestion become an action?
- Who authorized execution?
- What context was relied on?
- What happens when constraints conflict?
- How does the system fail safely?

This repository documents a deterministic model that answers those questions explicitly.

---

## What this repository provides

This repository defines and demonstrates a **deterministic action governance layer** that sits between:

**intent → execution**

Its primary function is to make execution behavior:
- explicit
- inspectable
- auditable
- fail-closed

The system enforces a strict lifecycle:

**proposal → decision → explicit commit → execution or refusal**

Refusal is treated as a correct and expected outcome.

---

## What this repository does NOT do

This repository intentionally avoids:

- autonomous behavior
- implicit execution
- agent frameworks
- intelligence claims
- UX design guidance
- automation abstractions
- long-lived permissions

If you are looking for an agent, this is not it.  
If you are looking for a safety primitive, you are in the right place.

---

## How to evaluate this work (recommended)

You do **not** need to read everything.

A minimal evaluation path:

1. **Read the guarantees**
   - See the “Guarantees” section in `README.md`
   - Confirm they are enforced by contract, not convention

2. **Inspect refusal behavior**
   - `docs/refusal_model.md`
   - `docs/failure_modes.md`
   Look for explicit refusal reasons and non-ambiguous outcomes

3. **Examine invariants**
   - `docs/invariants.md`
   These define what the system is *incapable* of doing

4. **Run the demos**
   ```bash
   ./v2/demo/scripts/run_all_demos.sh
