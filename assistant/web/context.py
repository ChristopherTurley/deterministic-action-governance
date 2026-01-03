# assistant/web/context.py
from __future__ import annotations

from typing import List, Dict, Any

from assistant.web.search import WebSource, web_search
from assistant.web.youtube import find_youtube_playlist, best_jazz_playlist_sources


def get_web_sources(query: str, max_results: int = 3) -> List[dict]:
    """
    Returns a list of dict sources with: title, url, snippet, provider.
    This is intentionally lightweight so the LLM can cite it.
    """
    q = (query or "").strip()
    if not q:
        return []

    low = q.lower()

    # YouTube specialized handling
    if "youtube" in low and ("playlist" in low or "play" in low or "jazz" in low):
        # If the prompt is generic jazz playlist request, we can shortcut
        if "jazz" in low and "playlist" in low:
            sources = best_jazz_playlist_sources(max_results=max_results)
        else:
            sources = find_youtube_playlist(q, max_results=max_results)
        return [s.__dict__ for s in sources]

    # Default: general web search
    sources = web_search(q, max_results=max_results)
    return [s.__dict__ for s in sources]


def format_sources_for_prompt(web_sources: List[dict]) -> str:
    """
    Formats sources to inject into the LLM prompt.
    Keep it compact, high signal.
    """
    if not web_sources:
        return ""

    lines = ["WEB SOURCES (use for facts, cite URLs):"]
    for i, s in enumerate(web_sources, start=1):
        title = s.get("title", "").strip()
        url = s.get("url", "").strip()
        snippet = s.get("snippet", "").strip()
        provider = s.get("provider", "web")
        if snippet:
            lines.append(f"{i}. {title} ({provider}) - {url}\n   Snippet: {snippet}")
        else:
            lines.append(f"{i}. {title} ({provider}) - {url}")
    return "\n".join(lines)

