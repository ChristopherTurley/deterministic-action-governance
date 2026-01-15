from __future__ import annotations

from typing import Dict


# Stable templates. Keep these short. No extra commentary.
# Keys are reason codes emitted by hats.
REASON_TEMPLATES: Dict[str, str] = {
    # Generic
    "context_stale_ttl_exceeded": "Refused: context is stale. Refresh the snapshot.",
    # Trading
    "risk_daily_loss_limit_reached_or_exceeded": "Refused: daily loss limit reached.",
    "trade_count_cap_reached_or_exceeded": "Refused: trade count cap reached.",
    "proposal_missing_required_key:max_loss": "Refused: proposal missing max loss.",
    "proposal_missing_required_key:invalidation": "Refused: proposal missing invalidation.",
    "proposal_missing_required_key:size": "Refused: proposal missing size.",
    "proposal_missing_required_key:entry_intent": "Refused: proposal missing entry intent.",
    "proposal_missing_required_key:time_constraint": "Refused: proposal missing time constraint.",
    # Focus
    "focus_no_tasks_remaining": "Refused: no tasks remaining in this focus session.",
    "focus_task_count_exceeds_cap": "Refused: task count exceeds cap.",
    "focus_task_count_exceeds_remaining": "Refused: task count exceeds remaining.",
    "focus_planned_minutes_exceeds_cap": "Refused: planned minutes exceed cap.",
    "focus_planned_minutes_exceeds_remaining": "Refused: planned minutes exceed remaining.",
}


def template_for(reason: str) -> str:
    # Drift reasons include a payload suffix; handle prefix.
    if reason.startswith("proposal_drift_requires_recommit:"):
        fields = reason.split(":", 1)[1]
        return "Re-commit required: proposal changed (" + fields + ")."

    if reason.startswith("context_missing_required_key:"):
        key = reason.split(":", 1)[1]
        return "Refused: context missing " + key + "."

    if reason.startswith("proposal_missing_required_key:"):
        key = reason.split(":", 1)[1]
        return "Refused: proposal missing " + key + "."

    if reason.startswith("unknown_hat:"):
        name = reason.split(":", 1)[1]
        return "Refused: unknown hat " + name + "."

    return REASON_TEMPLATES.get(reason, "Refused: policy rule triggered (" + reason + ").")

# --- Registry template coverage (v1) ---
# These templates exist to ensure deterministic rendering for all canonical INV_* reason codes.
# They are explanation-only and must never guide action.

REGISTRY_TEMPLATES_V1 = {
    # DESIGN
    "INV_DESIGN_BOUNDARY_VIOLATION": "Refused: design boundary violation.",
    "INV_DESIGN_MISSING_CONTEXT": "Refused: missing required context for design scope.",
    "INV_DESIGN_NO_OPTIMIZATION": "Refused: optimization/advice is out of scope for this hat.",

    # EDUCATION
    "INV_EDU_INTEGRITY_BOUNDARY_VIOLATION": "Refused: integrity boundary violation.",
    "INV_EDU_MISSING_CONTEXT": "Refused: missing required educational context.",
    "INV_EDU_NO_GRADING": "Refused: grading/evaluation is out of scope.",
    "INV_EDU_NO_SURVEILLANCE": "Refused: surveillance/monitoring is out of scope.",

    # ENGINEERING
    "INV_ENG_AUTHORITY_REQUIRED": "Refused: required authority was not present.",
    "INV_ENG_MISSING_CONTEXT": "Refused: missing required engineering context.",
    "INV_ENG_NO_ENFORCEMENT": "Refused: enforcement/automation is out of scope.",

    # EXECUTIVE
    "INV_EXEC_MISSING_CONTEXT": "Refused: missing required executive context.",
    "INV_EXEC_NO_ADVICE": "Refused: advice/optimization is out of scope.",
    "INV_EXEC_ROLE_AUTHORITY_REQUIRED": "Refused: required role authority was not present.",

    # FOCUS
    "INV_FOCUS_CONSTRAINT_VIOLATION": "Refused: focus/session constraint violation.",
    "INV_FOCUS_MISSING_CONTEXT": "Refused: missing required focus context.",
    "INV_FOCUS_NO_NUDGING": "Refused: nudging/behavior shaping is out of scope.",

    # HEALTHCARE
    "INV_HEALTH_CLINICIAN_AUTHORITY_REQUIRED": "Refused: clinician authority required.",
    "INV_HEALTH_MISSING_REQUIRED_CONTEXT": "Refused: missing required clinical context.",
    "INV_HEALTH_NO_DIAGNOSIS": "Refused: diagnosis is out of scope.",
    "INV_HEALTH_NO_TREATMENT_RECOMMENDATION": "Refused: treatment recommendation is out of scope.",

    # OPS
    "INV_OPS_MISSING_CHANGE_SUMMARY": "Refused: missing required change summary.",
    "INV_OPS_NO_BACKGROUND_RETRY": "Refused: background retry behavior is out of scope.",
    "INV_OPS_PRODUCTION_SCOPE_REQUIRES_CONFIRM": "Refused: production scope requires explicit confirmation.",
    "INV_OPS_REQUIRES_EXPLICIT_COMMIT": "Refused: explicit commit required.",

    # PLATFORM
    "INV_PLATFORM_NO_BACKGROUND_BEHAVIOR": "Refused: background behavior is out of scope.",
    "INV_PLATFORM_NO_PERMISSION_BROKERING": "Refused: permission brokering is out of scope.",

    # SPORTS
    "INV_SPORTS_AUTHORITY_REQUIRED": "Refused: required authority was not present.",
    "INV_SPORTS_MISSING_CONTEXT": "Refused: missing required sports context.",
    "INV_SPORTS_NO_OPTIMIZATION": "Refused: optimization/advice is out of scope.",

    # TRADING
    "INV_TRADING_INSTRUMENT_NOT_ALLOWED": "Refused: instrument not allowed.",
    "INV_TRADING_MAX_DAILY_LOSS_EXCEEDED": "Refused: max daily loss exceeded.",
    "INV_TRADING_MAX_LOSS_PER_TRADE_EXCEEDED": "Refused: max loss per trade exceeded.",
    "INV_TRADING_MAX_TRADES_PER_DAY_EXCEEDED": "Refused: max trades per day exceeded.",
    "INV_TRADING_MISSING_REQUIRED_FIELD": "Refused: missing required field.",
    "INV_TRADING_OUTSIDE_TIME_WINDOW": "Refused: outside allowed time window.",
    "INV_TRADING_OVERRIDE_REQUIRES_COMMIT": "Refused: override requires explicit commit.",
}
