from __future__ import annotations

from typing import Any, Dict

from assistant.tools.sports import get_games, format_sports_response
from assistant.core.source_actions import parse_open_source, wants_show_sources, build_sources_display

def is_sports_schedule_query(text: str) -> bool:
    t = (text or "").lower()
    triggers = [
        "games on", "games tonight", "games today", "who plays", "matchups", "scoreboard",
        "schedule", "what time do", "is playing", "are playing"
    ]
    sports_words = [
        "nhl", "nba", "wnba", "nfl", "mlb", "hockey", "basketball", "football", "baseball",
        "soccer", "premier league", "champions league", "ncaaf", "ncaam", "ncaaw"
    ]
    return any(x in t for x in triggers) and (any(w in t for w in sports_words) or "games" in t)

async def try_handle_sports(text: str, state: Any, say: Any, render: Any, open_url: Any | None = None) -> bool:
    """
    Wire this into runtime where you have:
      - say(str): speaks/logs
      - render(list[str]): prints to screen UI
      - open_url(url): optional
    """
    if not hasattr(state, "last_sources"):
        state.last_sources = []

    idx = parse_open_source(text)
    if idx is not None:
        sources = state.last_sources or []
        if not sources:
            msg = "I do not have a saved source from the last request. Ask for games again and I will attach sources."
            render([msg]); say(msg)
            return True
        if idx < 1 or idx > len(sources):
            msg = f"I have {len(sources)} sources saved. Say open source 1 through open source {len(sources)}."
            render(build_sources_display(sources)); say(msg)
            return True
        chosen: Dict[str, str] = sources[idx - 1]
        url = chosen.get("url")
        title = chosen.get("title", f"Source {idx}")
        if url and open_url:
            open_url(url)
            say(f"Opening {title}.")
        else:
            say("That source does not have a URL attached.")
        return True

    if wants_show_sources(text):
        render(build_sources_display(state.last_sources or []))
        say("Here are the sources I saved from the last request.")
        return True

    if is_sports_schedule_query(text):
        result = get_games(text)
        packaged = format_sports_response(result)
        state.last_sources = packaged.get("sources", [])
        render(packaged["display_lines"])
        say(packaged["spoken"])
        return True

    return False
