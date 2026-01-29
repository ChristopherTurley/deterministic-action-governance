# Governance Claims Substantiated
**VERA — Deterministic Action Governance**  
**Evaluated Artifact: Version-Locked**

---

## Purpose

This document defines the **governance claims substantiated** by successful execution of the VERA deterministic evaluation suite for the evaluated artifact version.

This document is **interpretive, not executable**.  
The evaluation suite is the executable evidence.

---

## Scope of Evaluation

The evaluation assesses **governance behavior**, not model performance or real-world outcomes.

Specifically, the evaluation examines:

- deterministic decision boundaries  
- explicit refusal and failure conditions  
- proposal versus commit separation  
- version-lock integrity  
- reproducible, audit-grade evidence generation  

The evaluation does **not** assess:

- model accuracy or optimization  
- runtime enforcement  
- production behavior  
- future behavior guarantees  

All evaluation activity occurs **offline**, under the buyer’s control.

---

## Governance Claims Substantiated

Successful completion of the evaluation suite (all tests passing) substantiates **all claims below**, for the evaluated artifact version only.

Each claim is supported by one or more deterministic tests in the evaluation suite.  
Individual tests may substantiate multiple claims.

---

### 1. Deterministic Governance Decisions

Given identical proposals, context, and rules, governance evaluation produces identical allow/refuse outcomes on every execution.

There is no probabilistic behavior or decision drift within the evaluated version.

---

### 2. Fail-Closed, Refusal-First Semantics

When required context, constraints, or invariants are missing, ambiguous, or violated, governance evaluation **refuses by default**.

Inaction and refusal are treated as correct and intentional governance outcomes.

---

### 3. Explicit, Inspectable Refusal Conditions

All refusals are explicit, deterministic, and recorded as evidence.

Silent failure, probabilistic degradation, or ambiguous outcomes are not permitted.

---

### 4. Proposal Versus Commit Separation

Proposals are evaluated without execution.

Execution requires an explicit, separate commit step and is never implied by evaluation alone.

This enforces human accountability boundaries.

---

### 5. No Implicit Side Effects

Governance evaluation produces no external actions, mutations, background execution, or runtime side effects.

Evaluation is safe to run repeatedly and independently.

---

### 6. Version-Locked Governance Logic

All evaluated governance logic, manifests, and constraints are immutable for the evaluated artifact version.

Governance behavior cannot change without re-evaluation of a new version.

---

### 7. Reproducible Evidence Generation

Evaluation outputs (logs, receipts, manifests) are deterministically generated and reproducible.

Evidence can be regenerated and compared across executions.

---

### 8. Independent Verification (Device-B)

The same evaluation can be re-executed on a second, independent machine with matching outputs.

This confirms the absence of hidden state, environment dependency, or vendor influence.

---

### 9. Binary Acceptance Criteria

Evaluation results are binary: **pass or fail**.

There is no scoring, ranking, or interpretive layer applied by the vendor.

Acceptance or rejection is determined solely by evidence.

---

## What Successful Evaluation Proves

A successful evaluation demonstrates that, **at the time of evaluation**:

- governance behavior is deterministic  
- refusal conditions are explicit and enforced  
- decision boundaries are inspectable and testable  
- evidence is reproducible and auditable  
- claims can be independently verified without vendor trust  

---

## What Evaluation Does Not Prove

Evaluation does not imply:

- runtime enforcement  
- future behavior guarantees  
- correctness outside evaluated conditions  
- system safety beyond the evaluated scope  

Governance evidence is **time-bound** to the evaluated artifact version.

---

## Intended Use as Evidence

The evaluated artifact and its outputs are intended to be retained as:

- independent governance verification evidence  
- audit and regulatory review material  
- internal risk and board documentation  

Retention of evidence should include:

- the evaluated archive  
- the checksum  
- the evaluation outputs  
- the applicable license for the evaluated version  

---

## Acceptance and Licensing Context

Licensing applies **only** to the evaluated artifact version.

Acceptance is an objective outcome based solely on evaluation results.

Rejection is a valid and expected outcome.

---

## Closing Statement

VERA does not ask to be trusted.

It provides deterministic, inspectable evidence so governance claims can be verified independently.
