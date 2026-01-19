# START HERE — Enterprise Deployment (Sidecar Model)

This repository contains two intentionally separate components.

## v2/ — Governance Reference Artifact (IMMUTABLE)
The v2 directory is a locked governance reference artifact proving:
- Deterministic evaluation
- Refusal-first semantics
- Receipt-based auditability
- Offline / Device-B verification

v2 is NOT a production service and must remain unchanged.

## Enterprise Sidecar — Operational Enforcement Layer
The enterprise sidecar is a deployable service that sits between AI systems
and external actions, deterministically allowing or refusing actions and
emitting signed, tamper-evident audit receipts.

AI / Agent → DAG Sidecar → External APIs / Tools / Payments
