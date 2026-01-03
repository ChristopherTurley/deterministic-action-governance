from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any

from assistant.router.core import route_text, RouteResult

MISSION = (
    "I'm VERA, a Voice-Enabled Reasoning Assistant designed to keep you moving. "
    "I understand what you say, what you're looking at, and what's coming next. "
    "I organize your day, anticipate priorities, and offer real-time guidance without distraction "
    "so you can stay focused and in execution mode."
)

STATE_PATH = Path("assistant_state.json")

@dataclass
class TextState:
    awake: bool = True
    top_priority: Optional[str] = None

def load_state() -> TextState:
    if STATE_PATH.exists():
        try:
            d = json.loads(STATE_PATH.read_text())
            return TextState(
                awake=bool(d.get("awake", True)),
                top_priority=d.get("top_priority"),
            )
        except Exception:
            pass
    return TextState()

def save_state(st: TextState) -> None:
    STATE_PATH.write_text(json.dumps({"awake": st.awake, "top_priority": st.top_priority}, indent=2))

def process_one(raw: str, *, wake_required: bool = True, priority_enabled: bool = True) -> str:
    st = load_state()
    rr: RouteResult = route_text(raw, wake_required=wake_required, priority_enabled=priority_enabled, awake=st.awake)

    if rr.kind == "NUDGE_WAKE":
        return "Say 'Hey Vera' first, then ask your question."

    if rr.kind == "SLEEP":
        st.awake = False
        save_state(st)
        return "Going to sleep. Say 'Hey Vera' to wake me."

    if rr.kind == "MISSION":
        return MISSION

    if rr.kind == "START_DAY":
        return "Alright. Give me your top priority and your first deadline."

    if rr.kind == "TIME":
        import datetime
        now = datetime.datetime.now()
        return f"It is {now.strftime('%-I:%M %p')}."

    if rr.kind == "PRIORITY_SET":
        st.top_priority = rr.meta.get("value")
        save_state(st)
        return f"Locked. Your top priority today is: {st.top_priority}."

    if rr.kind == "PRIORITY_GET":
        if not st.top_priority:
            return "You haven’t set a top priority yet. Say: 'my top priority today is ...'"
        return f"You said your top priority today is: {st.top_priority}."

    if rr.kind == "SPOTIFY":
        cmd = rr.meta.get("cmd")
        if cmd == "liked":
            return "Spotify: would open Liked Songs and start playing."
        if cmd == "pause":
            return "Spotify: would pause playback."
        if cmd == "resume":
            return "Spotify: would resume playback."
        if cmd == "play":
            q = rr.meta.get("query") or ""
            return f"Spotify: would search and play: {q!r}."
        return f"Spotify: {rr.meta}"

    if rr.kind == "OPEN_LINK":
        return f"Open requested: {rr.meta.get('target')}."

    if rr.kind == "WEB_LOOKUP":
        return f"Web lookup requested: {rr.meta.get('query') or rr.cleaned}"

    return "Ask me directly — I’ll answer."
