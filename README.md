# VERA — Deterministic Action Governance

VERA is a **deterministic governance layer** designed to sit between *intent* and *action*.

This repository is **not an AI agent**, **not an automation framework**, and **not a product demo**.

It is a **reference implementation** proving that:
- Actions can be governed deterministically
- Refusal and inaction can be correct outcomes
- Domain constraints can be enforced without hidden execution
- AI systems do not need autonomy to be useful

---

## Core Principles

VERA is built on the following invariants:

- **Fail-Closed by Default**  
  If something is unclear, missing, ambiguous, or unsafe — VERA refuses.

- **No Silent Execution**  
  Every allowed action must pass through an explicit decision boundary.

- **Deterministic Outcomes**  
  The same inputs produce the same decisions. No hidden state. No background behavior.

- **Refusals Are First-Class**  
  A refusal is a successful outcome, not an error.

- **Governance Before Capability**  
  This system exists to prove *control*, not convenience.

---

## Architecture Overview

VERA separates governance into three layers:

### 1. Core (Locked)

The core defines:
- Decision flow
- Proposal vs commit semantics
- Event structure
- Deterministic routing

The core **does not**:
- Execute side effects
- Call external services
- Perform automation

---

### 2. Hats — Domain Governance

A **Hat** represents governance rules for a specific domain (e.g. trading, focus, healthcare).

Each hat:
- Receives a proposal
- Returns a deterministic decision:
  - `ALLOW`
  - `REFUSE`
  - `REQUIRE_RECOMMIT`
- Provides explicit, namespaced reason codes

Important:
> A hat being present does **not** imply capability.

Many hats in this repository are **intentional fail-closed stubs**.  
These are not incomplete — they are **explicit refusals by design**.

---

### 3. Coats — Explanation Layer

A **Coat** is a non-decisional rendering layer.

It:
- Translates decisions into stable, human-readable output
- Preserves audit clarity
- Never changes outcomes
- Never adds intelligence

---

## Decision Lifecycle

1. **PROPOSE**
2. **COMMIT**
3. **DRIFT DETECTION**

Any drift requires explicit recommit.

---

## Status

Canonical locked state:


---

End of document.
