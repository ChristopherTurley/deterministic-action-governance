# Sidecar API v1

The sidecar is deployed as a proxy/sidecar service between an AI system and external actions.

Conceptual flow:
AI / Agent -> Sidecar (/v1/evaluate) -> External APIs (executed by the caller, not by the sidecar)

The sidecar:
- Evaluates proposals deterministically
- Returns ALLOW or REFUSE
- Emits a signed, tamper-evident receipt for every evaluation
- Does not execute actions

## Endpoints

### POST /v1/evaluate
Evaluates a proposed action.

Request body: JSON (see request schema)
Response body: JSON (see response schema)

### GET /healthz
Returns 200 if sidecar is running.

### GET /version
Returns engine version, build id, and current policy version.

## Determinism Requirements
- Request JSON is normalized for hashing:
  - UTF-8 JSON
  - keys sorted
  - no insignificant whitespace
- Sidecar hashes the canonicalized request into proposal_hash.
