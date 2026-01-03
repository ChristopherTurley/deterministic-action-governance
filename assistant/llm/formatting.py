from __future__ import annotations

from typing import List, Dict, Any


def add_uncertainty_language(answer: str, confidence: float) -> str:
    """
    Product rule:
    - Do NOT add robotic filler like "there may be ambiguity".
    - If confidence is low, keep it subtle and short (optional).
    """
    a = (answer or "").strip()
    if not a:
        return ""
    # Optional minimal hedge if extremely low confidence
    if confidence is not None and float(confidence) <= 0.20:
        return a + "\n\n(If you want, I can double-check with another source.)"
    return a


def format_citations(sources_used: List[Dict[str, Any]]) -> str:
    if not sources_used:
        return ""
    lines = []
    for i, s in enumerate(sources_used[:3], 1):
        title = (s.get("title") or "Source").strip()
        url = (s.get("url") or "").strip()
        if url:
            lines.append(f"{i}) {title} — {url}")
        else:
            lines.append(f"{i}) {title}")
    return "\n\nSources:\n" + "\n".join(lines)
