from __future__ import annotations

import requests
from bs4 import BeautifulSoup
from typing import Dict, List

HEADERS = {"User-Agent": "Mozilla/5.0"}


def web_search_duckduckgo(query: str, max_results: int = 3) -> List[Dict[str, str]]:
    """
    Returns list of {title, url} from DuckDuckGo HTML endpoint.
    """
    url = "https://duckduckgo.com/html/"
    resp = requests.post(url, data={"q": query}, headers=HEADERS, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    results: List[Dict[str, str]] = []

    for link in soup.select(".result__a")[:max_results]:
        href = (link.get("href") or "").strip()
        title = link.get_text(" ", strip=True)
        if href and title:
            results.append({"title": title, "url": href})

    return results


def fetch_page_text(url: str, max_chars: int = 2000) -> str:
    """
    Fetch a URL and extract readable paragraph text.
    """
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # Remove non-content tags
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    text = " ".join([p for p in paragraphs if p])
    return text[:max_chars]


def fetch_sources_for_query(query: str, max_results: int = 3) -> List[Dict[str, str]]:
    """
    Returns structured sources:
      [{ "title": ..., "url": ..., "text": ... }, ...]
    """
    results = web_search_duckduckgo(query, max_results=max_results)
    sources: List[Dict[str, str]] = []

    for r in results:
        try:
            text = fetch_page_text(r["url"])
        except Exception:
            text = ""
        sources.append({"title": r["title"], "url": r["url"], "text": text})

    return sources

