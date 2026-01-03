from __future__ import annotations

import re
import urllib.parse
import urllib.request
from typing import List

from assistant.services.web_search.base import WebSource


class DuckDuckGoSearch:
    """
    Keyless fallback search using DuckDuckGo HTML endpoint.
    Good for demos / out-of-box operation. Keep as fallback for production.
    """

    def __init__(self, user_agent: str = "Mozilla/5.0") -> None:
        self.user_agent = user_agent

    def search(self, query: str, max_results: int = 3) -> List[WebSource]:
        q = (query or "").strip()
        if not q:
            return []

        url = "https://duckduckgo.com/html/?" + urllib.parse.urlencode({"q": q})
        req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        results: List[WebSource] = []

        # Title: <a class="result__a" href="...">TITLE</a>
        for m in re.finditer(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>', html):
            href = m.group(1)
            title_html = m.group(2)

            title = re.sub(r"<.*?>", "", title_html)
            title = re.sub(r"\s+", " ", title).strip()

            snippet = ""
            tail = html[m.end(): m.end() + 900]
            snip_match = re.search(r'result__snippet[^>]*>(.*?)</', tail)
            if snip_match:
                snippet_html = snip_match.group(1)
                snippet = re.sub(r"<.*?>", "", snippet_html)
                snippet = re.sub(r"\s+", " ", snippet).strip()

            # Clean DDG redirect links
            if "duckduckgo.com/l/?" in href and "uddg=" in href:
                try:
                    parsed = urllib.parse.urlparse(href if href.startswith("http") else "https:" + href)
                    qs = urllib.parse.parse_qs(parsed.query)
                    if "uddg" in qs:
                        href = qs["uddg"][0]
                except Exception:
                    pass

            if href.startswith("//"):
                href = "https:" + href

            if href and title:
                results.append(WebSource(title=title, url=href, snippet=snippet, source="duckduckgo"))

            if len(results) >= max_results:
                break

        return results

