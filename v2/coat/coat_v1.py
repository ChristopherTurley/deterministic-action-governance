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

# --- Canonical string rendering (LOCKED SURFACE) ---
# Demos expect a stable, human-readable "coat_display" string.
# This does NOT change decision semantics; it only formats an already-rendered dict.

def _stable_lines_from_rendered(rendered: Dict[str, Any], event: Dict[str, Any]) -> str:
    # Deterministic ordering: fixed field order + sorted reasons
    typ = rendered.get("type") or event.get("type", "")
    hat = rendered.get("hat", "")
    stage = rendered.get("stage") or event.get("stage", "")
    decision = rendered.get("decision", "")
    reasons = rendered.get("reasons", []) or []
    try:
        reasons = sorted([str(r) for r in reasons])
    except Exception:
        reasons = [str(r) for r in reasons]

    lines = []
    lines.append(f"type: {typ}")
    lines.append(f"hat: {hat}")
    if stage:
        lines.append(f"stage: {stage}")
    lines.append(f"decision: {decision}")
    if reasons:
        lines.append("reasons:")
        for r in reasons:
            lines.append(f" - {r}")
    return "\n".join(lines)

def render_decision_v1(event: Dict[str, Any]) -> str:
    """
    Canonical coat entrypoint for demos.
    Returns stable, audit-legible, human-readable output.
    """
    rendered = render_hat_event(event)
    return _stable_lines_from_rendered(rendered, event)

# --- Canonical coat string rendering (LOCKED SURFACE) ---
# Demos expect a stable, human-readable string. This does not change any decision semantics.

