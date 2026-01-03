from __future__ import annotations

from typing import Callable, Dict

from assistant.router.types import RouteResult

Handler = Callable[[RouteResult, "App"], str]

def dispatch(app: "App", rr: RouteResult) -> str:
    handlers: Dict[str, Callable[[RouteResult], str]] = {
        "NUDGE_WAKE": app.handle_nudge_wake,
        "WAKE": app.handle_wake,
        "ASLEEP_IGNORE": app.handle_asleep_ignore,
        "SLEEP": app.handle_sleep,
        "MISSION": app.handle_mission,
        "TIME": app.handle_time,
        "SCREEN_SUMMARY": app.handle_screen_summary,
        "OPEN_LINK": app.handle_open_link,
        "PRIORITY_SET": app.handle_priority_set,
        "PRIORITY_GET": app.handle_priority_get,
        "START_DAY": app.handle_start_day,
        "WEB_LOOKUP": app.handle_web_lookup,
        "SPOTIFY": app.handle_spotify,
        "LLM_FALLBACK": app.handle_llm_fallback,
    }
    h = handlers.get(rr.kind, app.handle_llm_fallback)
    return h(rr)
