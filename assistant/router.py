from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Any, Dict, Optional

WAKE_RE = re.compile(r"\b(hey[\s,]+vera|vera)\b", re.I)

def clean_text(s: str) -> str:
    s = (s or "").strip()
    # normalize punctuation spacing
    s = re.sub(r"\s+", " ", s)
    return s

def strip_wake(s: str) -> str:
    s = WAKE_RE.sub("", s)
    s = re.sub(r"^[\s,]+|[\s,]+$", "", s)
    return s.strip()

@dataclass
class Route:
    name: str
    meta: Dict[str, Any]

def route(raw: str, *, wake_required: bool = True, is_awake: bool = True) -> Route:
    raw = clean_text(raw)
    has_wake = bool(WAKE_RE.search(raw))
    cleaned = clean_text(strip_wake(raw).lower())

    # If asleep, only wake phrase should work
    if not is_awake:
        if has_wake:
            return Route("WAKE", {"has_wake": True})
        return Route("SLEEP_BLOCK", {"has_wake": False})

    # Wake gating
    if wake_required and not has_wake:
        # Allow "open 2" etc without wake (optional convenience)
        if re.fullmatch(r"(open\s+\d+|open\s+it)", cleaned):
            return Route("OPEN_LINK", {"target": cleaned.replace("open ", ""), "has_wake": False})
        return Route("NUDGE_WAKE", {"has_wake": False, "requires_wake": True})

    # Wake-only utterance
    if cleaned in ("", "hey", "yeah", "yo", "hi"):
        return Route("WAKE_ACK", {"has_wake": has_wake})

    # Sleep
    if re.fullmatch(r"(sleep|go to sleep|vera sleep)", cleaned):
        return Route("SLEEP", {"has_wake": has_wake})

    # Mission
    if any(k in cleaned for k in ["mission", "what are you", "who are you", "what do you do"]):
        return Route("MISSION", {"has_wake": has_wake})

    # Start my day
    if any(k in cleaned for k in ["start my day", "todays rundown", "today's rundown", "daily brief", "daily briefing"]):
        return Route("START_DAY", {"has_wake": has_wake})

    # Priority set
    m = re.search(r"(my\s+(top\s+)?priority\s+(today\s+)?is)\s+(.*)$", cleaned)
    if m and m.group(4).strip():
        return Route("PRIORITY_SET", {"has_wake": has_wake, "value": m.group(4).strip().rstrip(".")})

    # Priority get (THIS IS WHAT YOU WERE MISSING)
    if any(k in cleaned for k in [
        "what's my top priority", "what is my top priority", "whats my top priority",
        "what's my priority", "what is my priority", "whats my priority",
        "what did i just say my priority was", "what did i say my priority was",
        "remind me my priority", "tell me my priority"
    ]):
        return Route("PRIORITY_GET", {"has_wake": has_wake})

    # Time
    if any(k in cleaned for k in ["what time is it", "time is it", "tell me the time"]):
        return Route("TIME", {"has_wake": has_wake})

    # Screen
    if any(k in cleaned for k in ["summarize my screen", "summarize this", "what's on my screen", "what is on my screen"]):
        return Route("SCREEN_SUMMARY", {"has_wake": has_wake})

    # Spotify (play / liked / pause / resume)
    if "spotify" in cleaned or any(cleaned.startswith(x) for x in ["play ", "pause", "resume"]):
        # liked songs
        if "liked songs" in cleaned or "my liked songs" in cleaned:
            return Route("SPOTIFY", {"has_wake": has_wake, "cmd": "liked", "query": None})
        if cleaned in ("pause", "pause music", "pause playback"):
            return Route("SPOTIFY", {"has_wake": has_wake, "cmd": "pause", "query": None})
        if cleaned in ("resume", "continue", "play", "resume music"):
            return Route("SPOTIFY", {"has_wake": has_wake, "cmd": "resume", "query": None})

        # "play X on spotify" / "play X"
        m = re.search(r"^play\s+(.*?)(\s+on\s+spotify)?$", cleaned)
        if m:
            q = (m.group(1) or "").strip()
            q = q.replace("spotify", "").strip()
            if q:
                return Route("SPOTIFY", {"has_wake": has_wake, "cmd": "play", "query": q})
        # fallback: still spotify route but no query
        return Route("SPOTIFY", {"has_wake": has_wake, "cmd": "play", "query": ""})

    # Web lookup (explicit only)
    if any(k in cleaned for k in ["search the web", "look up", "find the latest", "what nhl games are on"]):
        return Route("WEB_LOOKUP", {"has_wake": has_wake, "query": cleaned})

    return Route("LLM_FALLBACK", {"has_wake": has_wake})
