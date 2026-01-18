# Ops Incident Hat v1 (FROZEN)

Hat ID: OPS_INCIDENT_HAT_V1
Prefix: INV_OPS_

NON-NEGOTIABLES
- No execution
- No automation
- No background behavior
- Deterministic outcomes only

Context keys (required)
- incident_mode (bool)
- severity (SEV0/1/2/3)
- change_freeze (bool)
- context_as_of_ts
- context_ttl_seconds

Proposal keys (required)
- op_type (deploy/config_change/restart/access_change)
- risk_level (LOW/MEDIUM/HIGH)
- now_ts
- summary

Core semantics
- Fail closed on missing context / malformed input / stale context
- During incident + change_freeze:
  - refuse HIGH risk ops
  - refuse deploy/config/access by default
- Commit requires exact match; drift => REQUIRE_RECOMMIT

Reasons (all prefixed)
- INV_OPS_missing_context_keys:<k>
- INV_OPS_context_stale
- INV_OPS_incident_freeze_blocks_high_risk_ops
- INV_OPS_incident_freeze_blocks_risky_op_type:<op>
- INV_OPS_proposal_not_allowed
- INV_OPS_proposal_drift_requires_recommit:<keys>
- INV_OPS_malformed_*
