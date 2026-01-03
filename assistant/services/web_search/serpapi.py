from __future__ import annotations
import requests
from typing import List
from assistant.services.web_search.base import WebSource


class SerpApiSearch:
    name = "serpapi"

    def __init__(self, api_key: str):
        self.api_key = (api_key or "").strip()

    def search(self, query: str, max_results: int = 3) -> List[WebSource]:
        if not self.api_key:
            return []

        url = "https://serpapi.com/search.json"
        params = {
            "engine": "google",
            "q": query,
            "api_key": self.api_key,
            "num": max_results,
        }
        r = requests.get(url, params=params, timeout=12)
        r.raise_for_status()
        data = r.json()

        organic = data.get("organic_results") or []
        out: List[WebSource] = []
        for item in organic[:max_results]:
            title = item.get("title") or ""
            link = item.get("link") or ""
            snippet = item.get("snippet") or ""
            if title and link:
                out.append(WebSource(title=title, url=link, snippet=str(snippet), source=self.name))
        return out
