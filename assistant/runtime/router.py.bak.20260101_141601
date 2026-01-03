from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional, Dict, Any

from assistant.utils.text import normalize_text
from assistant.controllers.spotify_rules import classify_spotify

# Deterministic mission triggers (same idea as main.py)
MISSION_TRIGGERS = (
    "what is your purpose",
    "what's your purpose",
    "what is your mission",
    "what's your mission",
    "mission statement",
    "tell me your mission",
    "tell me about yourself",
    "what do you do",
    "why do you exist",
    "what are you",
    "who are you",
)

PRIORITY_SET = [
    re.compile(r"^(?:my\s+)?(?:top|main)\s+priority\s+today\s+is\s+(.+)$", re.I),
    re.compile(r"^(?:my\s+)?priority\s+today\s+is\s+(.+)$", re.I),
]
PRIORITY_GET = [
    re.compile(r"what did i (?:just )?say my (?:top|main )?priority was", re.I),
    re.compile(r"what'?s my (?:top|main )?priority", re.I),
    re.compile(r"remind me my (?:top|main )?priority", re.I),
]

@dataclass
class Route:
    name: str
    payload: Optional[Dict[str, Any]] = None

def route_intent(user_input: str) -> Route:
    ui = normalize_text(user_input)

    # Spotify deterministic
    sp = classify_spotify(user_input)
    if sp.handled:
        return Route("SPOTIFY", {"action": sp})

    # Mission deterministic
    if any(t in ui for t in MISSION_TRIGGERS):
        return Route("MISSION")

    # Daily brief commands
    if "start my day" in ui or "daily brief" in ui or "rundown" in ui:
        return Route("START_MY_DAY")

    if "schedule my day" in ui or "plan my day" in ui or "time block" in ui:
        return Route("SCHEDULE_MY_DAY")

    # Priority set/get
    raw = (user_input or "").strip()
    for p in PRIORITY_SET:
        m = p.match(raw)
        if m:
            val = (m.group(1) or "").strip(" .,!?:;")
            return Route("PRIORITY_SET", {"value": val})

    if any(p.search(raw) for p in PRIORITY_GET):
        return Route("PRIORITY_GET")

    # Web lookup triggers (simple keyword)
    if any(k in ui for k in ["search the web", "look up", "latest", "today", "news"]):
        return Route("WEB_LOOKUP", {"query": user_input})

    return Route("FALLBACK")
