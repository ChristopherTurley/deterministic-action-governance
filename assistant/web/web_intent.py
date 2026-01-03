from __future__ import annotations

import re

def needs_web_lookup(user_input: str) -> bool:
    """
    Product-grade web intent:
    - Only search web when it is actually needed.
    - Never search for tiny fragments, pure numbers, or generic commands.
    """
    t = (user_input or "").strip().lower()
    t = re.sub(r"\s+", " ", t)

    if not t:
        return False

    # Screen-related requests should not force web search.
    screen_markers = [
        "on my screen", "what's on my screen", "whats on my screen",
        "what am i looking at", "read the first", "summarize what is on my screen",
        "summarize my screen", "summarize this page", "this article"
    ]
    if any(m in t for m in screen_markers):
        return False

    # Local-only: time/date/basic system queries (never web)
    local_markers = [
        "what time is it", "current time", "time is it",
        "what day is it", "today's date", "todays date", "date today"
    ]
    if any(m in t for m in local_markers):
        return False

    # Pure numbers or very short queries are not web-worthy.
    if re.fullmatch(r"\d+(?:\.\d+)?", t):
        return False
    if len(t) < 5:
        return False

    # Generic filler queries should not go to web
    junk = {"summarize", "open it", "open that", "show me", "pull it up", "continue"}
    if t in junk:
        return False

    # If user explicitly says search/look up/news, we do it.
    explicit = ["search", "look up", "lookup", "google", "find", "news", "latest", "today"]
    if any(w in t for w in explicit):
        return True

    # If it’s a fact question likely requiring current info, allow web.
    # Keep this conservative.
    facty = ["who is", "what is", "price", "stock", "schedule", "score", "earnings", "release date"]
    if any(w in t for w in facty):
        return True

    return False
