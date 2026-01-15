from __future__ import annotations

from typing import Any, Dict, List

from v2.coat.templates_v1 import template_for


def render_hat_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Coat v1: render a hat decision event into stable operator-facing text.

    Input: ledger-like HAT_DECISION event dict.
    Output:
      - decision: unchanged
      - reasons: unchanged
      - spoken: short, stable sentence
      - display: short, stable multi-line text (if needed)
    """
    decision = event.get("decision", "")
    hat = event.get("hat", "")
    stage = event.get("stage", "")
    reasons = event.get("reasons", []) or []

    lines: List[str] = []
    if decision == "ALLOW":
        lines.append("Allowed.")
    elif decision == "REFUSE":
        lines.append("Refused.")
    elif decision == "REQUIRE_RECOMMIT":
        lines.append("Re-commit required.")
    else:
        lines.append("Decision: " + str(decision) + ".")

    # Add first reason as the primary explanation; include additional reasons as bullets.
    if reasons:
        primary = template_for(str(reasons[0]))
        lines.append(primary)
        if len(reasons) > 1:
            for r in reasons[1:]:
                lines.append("- " + template_for(str(r)))

    # Include minimal metadata line for debugging without noise.
    meta = "Hat: " + str(hat) + " | Stage: " + str(stage)

    display = "\n".join(lines + [meta])
    spoken = " ".join(lines[:2]) if len(lines) >= 2 else lines[0]

    return {
        "decision": decision,
        "reasons": list(reasons),
        "spoken": spoken,
        "display": display,
        "hat": hat,
        "stage": stage,
    }
