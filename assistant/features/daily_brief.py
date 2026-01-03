from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class CalendarEvent:
    start: str
    title: str
    location: str = ""

@dataclass
class DailyBrief:
    greeting: str
    local_time: str
    weather_line: str
    calendar_lines: List[str]
    plan_blocks: List[str]
    close: str

def _fmt_time_now() -> str:
    return dt.datetime.now().strftime("%I:%M %p").lstrip("0")

def build_plan_blocks(priority: Optional[str]) -> List[str]:
    # Ruthless, simple, deterministic template.
    pr = (priority or "").strip()
    if pr:
        core = f"Top Priority: {pr}."
    else:
        core = "Top Priority: (not set). Say: 'my top priority today is ...'"

    return [
        f"Morning: {core} Knock out the hardest 60–90 minutes first. No distractions.",
        "Midday: Meetings + admin. If it doesn’t move the goal, it gets cut.",
        "Afternoon: Deep work block #2. Close loops. Ship something."
    ]

def render_brief(profile_name: str, priority: Optional[str], weather_line: str, events: List[CalendarEvent]) -> DailyBrief:
    now = _fmt_time_now()
    greeting = f"Welcome back, {profile_name}. Today’s rundown is ready."
    cal_lines = []
    if events:
        cal_lines.append("Calendar:")
        for e in events[:5]:
            loc = f" — {e.location}" if e.location else ""
            cal_lines.append(f"- {e.start} {e.title}{loc}")
    else:
        cal_lines.append("Calendar: No events detected (Phase 1: add calendar integration next).")

    plan = build_plan_blocks(priority)
    close = "Want me to schedule this against deadlines and priority? Say: 'schedule my day'."
    return DailyBrief(
        greeting=greeting,
        local_time=f"Local time: {now}",
        weather_line=weather_line,
        calendar_lines=cal_lines,
        plan_blocks=plan,
        close=close,
    )

def is_start_my_day(text: str) -> bool:
    t = (text or "").lower()
    return ("start my day" in t) or ("daily brief" in t) or ("rundown" in t)

def is_schedule_my_day(text: str) -> bool:
    t = (text or "").lower()
    return ("schedule my day" in t) or ("plan my day" in t) or ("time block" in t)
