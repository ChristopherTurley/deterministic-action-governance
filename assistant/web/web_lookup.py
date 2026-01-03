from __future__ import annotations

import re
import textwrap
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import List


@dataclass
class WebResult:
    title: str
    url: str
    snippet: str = ""


_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"


def _fetch(url: str, timeout: int = 12) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="ignore")


def _strip_tags(s: str) -> str:
    s = re.sub(r"<.*?>", "", s)
    s = s.replace("&amp;", "&").replace("&quot;", '"').replace("&#39;", "'")
    return re.sub(r"\s+", " ", s).strip()


def _is_ad_url(u: str) -> bool:
    # DuckDuckGo ad/redirect patterns
    u = (u or "").lower()
    return (
        "duckduckgo.com/y.js" in u
        or "ad_provider" in u
        or "ad_domain" in u
        or "aclick" in u
        or "utm_" in u and "duckduckgo.com/l/" in u
    )


def search_duckduckgo(query: str, *, limit: int = 3) -> List[WebResult]:
    q = urllib.parse.quote_plus(query)
    url = f"https://duckduckgo.com/html/?q={q}"
    html = _fetch(url)

    link_re = re.compile(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>', re.I | re.S)
    snippet_re = re.compile(r'<a[^>]+class="result__snippet"[^>]*>(.*?)</a>|<div[^>]+class="result__snippet"[^>]*>(.*?)</div>', re.I | re.S)

    links = link_re.findall(html)
    snippets = snippet_re.findall(html)

    raw_results: List[WebResult] = []
    for i, (href, title_html) in enumerate(links):
        title = _strip_tags(title_html)
        snip = ""
        if i < len(snippets):
            sn = snippets[i][0] or snippets[i][1] or ""
            snip = _strip_tags(sn)
        if title and href:
            raw_results.append(WebResult(title=title, url=href, snippet=snip))

    # Filter ads and keep first organic results
    results: List[WebResult] = []
    for r in raw_results:
        if _is_ad_url(r.url):
            continue
        results.append(r)
        if len(results) >= limit:
            break

    # If filtering wiped everything (rare), fall back to raw
    if not results:
        results = raw_results[:limit]

    return results


def spoken_compact(results: List[WebResult]) -> str:
    # Speak titles, not ad snippets
    titles = [r.title for r in results if r.title][:3]
    if not titles:
        return "I found results, but couldn’t read titles cleanly."
    lines = []
    for i, t in enumerate(titles, start=1):
        t = textwrap.shorten(t, width=70, placeholder="…")
        lines.append(f"{i}. {t}")
    return "Here are three sources: " + " / ".join(lines)


def summarize(query: str, results: List[WebResult]) -> str:
    # Very short summary from snippets (optional)
    parts = [r.snippet for r in results if r.snippet]
    blob = " ".join(parts).strip()
    if not blob:
        return ""
    return textwrap.shorten(blob, width=160, placeholder="…")
