# Executive Hat v1 (FROZEN)

STATUS
- Hat ID: EXECUTIVE_HAT_V1
- State: FROZEN (once tagged)
- Authority: NONE
- Execution: NONE
- Advisory: NONE

SCOPE (LOCKED)
Executive Hat v1 is a governance-only classifier for executive decision intents.
It does not execute actions, send communications, share data, or provide advice.
Refusal and inaction are correct outcomes.

INPUT CONTRACT (LOCKED)
Context:
- role
- approval_limit_usd
- approvals_used_today
- approval_count_cap
- context_as_of_ts
- context_ttl_seconds
- policy_mode

Proposal / Commit:
- request_type: spend | share | comms | hire | strategy
- amount_usd
- data_classification: public | internal | confidential | restricted
- external_recipient: true|false
- now_ts
- summary

DECISION SEMANTICS
- PROPOSE:
  - REFUSE if context missing, stale, sensitive external sharing, restricted mode, approval caps, or spend limit exceeded
  - ALLOW otherwise
- COMMIT:
  - REFUSE if proposal not allowed
  - REQUIRE_RECOMMIT if any commit drift from proposal
  - ALLOW if identical and proposal allowed

REASON TOKENS (LOCKED)
- missing_context_keys:<key>
- context_stale
- restricted_mode_blocks_external_comms_or_sharing
- external_sharing_blocked_for_sensitive_data
- approval_count_cap_reached_or_exceeded
- spend_exceeds_approval_limit
- proposal_drift_requires_recommit:<keys>
- proposal_not_allowed
- malformed_input / malformed_* fields
