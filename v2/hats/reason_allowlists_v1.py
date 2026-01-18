"""Reason allowlists v1 (LOCKED)

Goal:
- Prevent silent addition/mutation of reason tokens (audit surface).
- Each hat's reasons must be:
  - correctly prefixed (already covered by other tests)
  - token-listed here (this file is versioned)

Rule:
- Adding a new reason token requires bumping hat version or explicit governance change.
"""

from __future__ import annotations

# Token allowlists are stored WITHOUT the per-hat prefix.
# For a reason string like "INV_EXEC_missing_context_keys:role",
# the token is "missing_context_keys" and may include a suffix after ":".

ALLOWLISTS_V1 = {
    "TRADING_HAT_V1": {
        "missing_context_keys",
        "context_stale",
        "risk_daily_loss_limit_reached_or_exceeded",
        "trade_count_cap_reached_or_exceeded",
        "instrument_mismatch_with_context",
        "proposal_not_allowed",
        "proposal_drift_requires_recommit",
        "malformed_input",
        "malformed_proposal",
        "malformed_timestamps",
    },
    "EXECUTIVE_HAT_V1": {
        "missing_context_keys",
        "context_stale",
        "proposal_not_allowed",
        "proposal_drift_requires_recommit",
        "malformed_input",
        "malformed_proposal",
        "malformed_timestamps",
        "approval_count_cap_reached_or_exceeded",
        "spend_exceeds_approval_limit",
        "restricted_mode_blocks_external_comms_or_sharing",
        "external_sharing_blocked_for_sensitive_data",
        "proposal_not_allowed",
    },
    "OPS_INCIDENT_HAT_V1": {
        "missing_context_keys",
        "context_stale",
        "incident_freeze_blocks_high_risk_ops",
        "incident_freeze_blocks_risky_op_type",
        "proposal_not_allowed",
        "proposal_drift_requires_recommit",
        "malformed_input",
        "malformed_proposal",
        "malformed_timestamps",
        "malformed_incident_fields",
    },
    "HEALTHCARE_HAT_V1": {
        "missing_context_keys",
        "context_stale",
        "clinical_advice_or_diagnosis_disallowed",
        "restricted_mode_blocks_sensitive_health_data",
        "proposal_not_allowed",
        "proposal_drift_requires_recommit",
        "malformed_input",
        "malformed_proposal",
        "malformed_timestamps",
        "malformed_request_fields",
    },
}
