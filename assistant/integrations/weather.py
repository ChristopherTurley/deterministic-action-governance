from __future__ import annotations

from typing import Optional, List
from assistant.services.web_search.aggregator import FallbackWebSearch
from assistant.services.web_search.base import WebSource

def get_weather_line(web_search: FallbackWebSearch, location_hint: str = "my location") -> str:
    """
    Phase 1: Web lookup. Later: proper weather API + location.
    """
    query = f"weather today {location_hint}"
    sources: List[WebSource] = web_search.search(query, max_results=2) or []
    if not sources:
        return "Weather: unavailable (web lookup failed)."
    # Keep it short; we only need a demo line.
    top = sources[0]
    snippet = (top.snippet or top.title or "").strip()
    snippet = " ".join(snippet.split())[:140]
    return f"Weather: {snippet}"
