from __future__ import annotations

import re
from typing import List, Optional

from assistant.web.search import WebSource, web_search


def _normalize(t: str) -> str:
    return re.sub(r"\s+", " ", (t or "").strip().lower())


def _looks_like_playlist(title: str, url: str) -> bool:
    t = _normalize(title)
    u = (url or "").lower()
    if "playlist" in t:
        return True
    # Common YouTube playlist URL patterns
    return ("list=" in u) or ("/playlist" in u)


def find_youtube_playlist(query: str, max_results: int = 5) -> List[WebSource]:
    """
    Finds YouTube playlists via general web search.
    Returns WebSource entries that can be cited.
    """
    q = (query or "").strip()
    if not q:
        return []

    # Bias toward playlists and YouTube results.
    # Example: site:youtube.com jazz playlist most popular
    search_q = f"site:youtube.com {q} playlist"
    sources = web_search(search_q, max_results=max_results * 2)

    # Filter for likely playlist links
    playlists: List[WebSource] = []
    for s in sources:
        if _looks_like_playlist(s.title, s.url):
            playlists.append(s)
        if len(playlists) >= max_results:
            break

    return playlists


def best_jazz_playlist_sources(max_results: int = 3) -> List[WebSource]:
    """
    Convenience for the user’s example.
    We approximate "most liked" with "most popular/most viewed" via search ranking.
    """
    query = "jazz playlist most popular most viewed"
    return find_youtube_playlist(query, max_results=max_results)

