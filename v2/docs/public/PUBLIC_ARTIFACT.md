# PUBLIC ARTIFACT — VERA Governance Reference

This repository is a deterministic governance reference artifact.
It is designed to be audited, cloned, and validated without trust.

## What this is
- Deterministic action-governance patterns
- Fail-closed refusal semantics
- Audit artifacts (receipts + diffs)
- Portable NDA validation packs runnable on an offline auditor machine

## What this is not
- Not a trading bot
- Not an execution engine
- Not automation
- Not advice
- Not probabilistic or adaptive behavior

## Trust model
- Receipts are authoritative
- Text output is non-authoritative
- Any mismatch, drift, or validation failure is a correct stop signal

## Device model
- Device A: generator/build machine
- Device B: auditor machine
  - no internet
  - no repo trust
  - no mutable state assumptions
  - receipts validated by schema + hash + diff

## Trading Gate Pack v1
Location:
- v2/nda/trading_gate_pack_v1

Provides:
- refusal code registry (policy)
- receipt schema
- reference receipts
- offline validator
- diff scripts

Daily use posture:
- Validate receipt schema
- Verify hashes
- Diff against the matching reference receipt
- Any failure means stop

## Publishing posture
This repo is safe to publish because it contains governance surfaces only.
No secrets, no endpoints, no strategies, no thresholds, and no side effects.

