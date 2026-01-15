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
