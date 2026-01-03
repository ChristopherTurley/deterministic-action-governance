from __future__ import annotations

from typing import List, Optional, Protocol

from assistant.services.web_search.base import WebSource


class SearchProvider(Protocol):
    def search(self, query: str, max_results: int = 3) -> List[WebSource]:
        ...


class FallbackWebSearch:
    """
    Tries providers in order. Returns the first non-empty result set.
    Records which provider succeeded in `last_provider_used`.
    """

    def __init__(self, providers: List[SearchProvider]) -> None:
        self.providers = providers
        self.last_provider_used: Optional[str] = None

    def search(self, query: str, max_results: int = 3) -> List[WebSource]:
        self.last_provider_used = None
        q = (query or "").strip()
        if not q:
            return []

        for p in self.providers:
            name = p.__class__.__name__
            try:
                out = p.search(q, max_results=max_results)
                if out:
                    self.last_provider_used = name
                    return out
            except Exception:
                continue

        return []

