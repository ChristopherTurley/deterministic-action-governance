# assistant/web/search.py
from __future__ import annotations

import time
import re
from dataclasses import dataclass
from typing import List, Optional

import requests
from bs4 import BeautifulSoup


@dataclass
class WebSource:
    title: str
    url: str
    snippet: str = ""
    provider: str = "duckduckgo"
    fetched_at: float = 0.0


def _clean_text(text: str) -> str:
    text = (text or "").strip()
    text = re.sub(r"\s+", " ", text)
    return text


def _build_soup(html: str) -> BeautifulSoup:
    # Prefer lxml if installed; fallback safely
    try:
        return BeautifulSoup(html, "lxml")
    except Exception:
        return BeautifulSoup(html, "html.parser")


def duckduckgo_search(query: str, max_results: int = 5, timeout_s: int = 12) -> List[WebSource]:
    """
    More resilient DDG HTML search:
    - Try POST to /html
    - If 0 results, try GET to /html (some environments behave differently)
    - Use multiple selector strategies
    """
    q = (query or "").strip()
    if not q:
        return []

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    def parse(html: str) -> List[WebSource]:
        soup = _build_soup(html)

        results: List[WebSource] = []

        # Strategy 1: classic DDG html layout
        blocks = soup.select(".result")
        # Strategy 2: fallback selectors (layout variations)
        if not blocks:
            blocks = soup.select("div.result") or soup.select("div.results > div")

        for b in blocks:
            a = b.select_one("a.result__a") or b.select_one("a[href]")
            if not a:
                continue

            title = _clean_text(a.get_text())
            href = (a.get("href") or "").strip()

            sn = b.select_one(".result__snippet") or b.select_one(".snippet") or b.select_one("div")
            snippet = _clean_text(sn.get_text() if sn else "")

            # quality checks
            if not title or not href:
                continue
            if not href.startswith("http"):
                continue

            results.append(
                WebSource(
                    title=title,
                    url=href,
                    snippet=snippet,
                    provider="duckduckgo",
                    fetched_at=time.time(),
                )
            )
            if len(results) >= max_results:
                break

        return results

    # Attempt 1: POST
    try:
        r = requests.post("https://duckduckgo.com/html/", data={"q": q}, headers=headers, timeout=timeout_s)
        r.raise_for_status()
        out = parse(r.text)
        if out:
            return out
    except Exception as e:
        print("[SEARCH] POST error:", e)

    # Attempt 2: GET fallback
    try:
        r = requests.get("https://duckduckgo.com/html/", params={"q": q}, headers=headers, timeout=timeout_s)
        r.raise_for_status()
        out = parse(r.text)
        if out:
            return out

        # Debug: If still nothing, print a short clue (helps diagnose bot-block page)
        print("[SEARCH] 0 results; page starts with:")
        print(r.text[:200].replace("\n", " "))
    except Exception as e:
        print("[SEARCH] GET error:", e)

    return []


def web_search(query: str, max_results: int = 5) -> List[WebSource]:
    return duckduckgo_search(query, max_results=max_results)

