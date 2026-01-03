from __future__ import annotations
import requests
from typing import List
from assistant.services.web_search.base import WebSource


class TavilySearch:
    name = "tavily"

    def __init__(self, api_key: str):
        self.api_key = (api_key or "").strip()

    def search(self, query: str, max_results: int = 3) -> List[WebSource]:
        if not self.api_key:
            return []

        url = "https://api.tavily.com/search"
        payload = {
            "api_key": self.api_key,
            "query": query,
            "max_results": max_results,
            "include_answer": False,
            "include_raw_content": False,
        }
        r = requests.post(url, json=payload, timeout=12)
        r.raise_for_status()
        data = r.json()

        results = data.get("results") or []
        out: List[WebSource] = []
        for item in results[:max_results]:
            title = item.get("title") or ""
            link = item.get("url") or ""
            snippet = item.get("content") or ""
            if title and link:
                out.append(WebSource(title=title, url=link, snippet=str(snippet), source=self.name))
        return out
