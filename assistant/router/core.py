from __future__ import annotations

import re
from typing import Dict, Tuple

from assistant.router.types import RouteResult
from assistant.controllers.spotify_rules import classify_spotify

# Accept common ASR variants
_WAKE_RE = re.compile(
    r"^\s*(hey\s+(vera|viera|veera|vieira|avera|ferra|havira)|vera|viera|veera|vieira|avera|ferra|havira)\b[\s,]*",
    re.IGNORECASE,
)

def _strip_wake(raw: str) -> Tuple[bool, str]:
    s = (raw or "").strip()
    m = _WAKE_RE.match(s)
    if not m:
        return False, s
    return True, s[m.end():].strip()

def _norm(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s

def _cmd(s: str) -> str:
    # For exact command matching, strip common trailing punctuation
    return (s or "").strip().strip(" \t\r\n.,!?;:")

def _is_open_link(c: str) -> Dict | None:
    m = re.match(r"^open\s+(\d+)$", c)
    if m:
        return {"target": int(m.group(1))}
    if c in ("open it", "open"):
        return {"target": "it"}
    return None

def route_text(
    raw: str,
    *,
    wake_required: bool = True,
    priority_enabled: bool = True,
    awake: bool = True,
) -> RouteResult:
    has_wake, stripped = _strip_wake(raw)
    cleaned = _norm(stripped)
    cmd = _cmd(cleaned)

    # --- Phase B micro-patch: wake-only + wake+help handling ---
    # If the user only says the wake phrase, treat it as WAKE.
    if has_wake and cmd == "":
        return RouteResult(kind="WAKE", meta={}, cleaned=cleaned, requires_wake=False, raw=raw)

    # If the user wakes and asks for help/capabilities, map to MISSION (handled in runtime).
    if has_wake and cmd in ("what can you do", "what do you do", "help", "what are you"):
        return RouteResult(kind="MISSION", meta={}, cleaned=cleaned, requires_wake=True, raw=raw)
    # --- end micro-patch ---

    if not awake:
        if has_wake or cmd in ("wake", "wake up"):
            return RouteResult(kind="WAKE", meta={}, cleaned=cleaned, requires_wake=False, raw=raw)
        return RouteResult(kind="ASLEEP_IGNORE", meta={}, cleaned=cleaned, requires_wake=False, raw=raw)

    open_meta = _is_open_link(cmd)
    if open_meta:
        return RouteResult(kind="OPEN_LINK", meta=open_meta | {"has_wake": has_wake}, cleaned=cleaned, requires_wake=False, raw=raw)

    if wake_required and not has_wake:
        return RouteResult(kind="NUDGE_WAKE", meta={"requires_wake": True}, cleaned=cleaned, requires_wake=True, raw=raw)

    if cmd in ("sleep", "go to sleep", "vera sleep", "viera sleep", "veera sleep"):
        return RouteResult(kind="SLEEP", meta={}, cleaned=cleaned, requires_wake=False, raw=raw)

    if cmd in ("what time is it", "time", "tell me the time", "what's the time"):
        return RouteResult(kind="TIME", meta={}, cleaned=cleaned, requires_wake=True, raw=raw)

    if any(x in cleaned for x in ("what are you", "your mission", "mission statement", "who are you")):
        return RouteResult(kind="MISSION", meta={}, cleaned=cleaned, requires_wake=True, raw=raw)

    if "summarize my screen" in cleaned or cmd in ("summarize", "what's on my screen"):
        return RouteResult(kind="SCREEN_SUMMARY", meta={}, cleaned=cleaned, requires_wake=True, raw=raw)

    if priority_enabled:
        m = re.match(r"^(my\s+)?(top|main|number one)\s+priority(\s+today|\s+for the day)?\s+(is|=)\s+(.+)$", cleaned)
        if m:
            value = m.group(5).strip(" .")
            return RouteResult(kind="PRIORITY_SET", meta={"value": value}, cleaned=cleaned, requires_wake=True, raw=raw)

        if re.match(r"^what did i (just )?say my (top )?priority was\??$", cleaned) or re.match(r"^what('?s| is) my (top )?priority\??$", cleaned):
            return RouteResult(kind="PRIORITY_GET", meta={}, cleaned=cleaned, requires_wake=True, raw=raw)

# --- Phase C micro-patch: tolerate partial START_DAY ---
    # Accept partial ASR fragments like 'start my-' when wake is present
    if has_wake and (cmd.startswith('start my') or cleaned.startswith('start my')):
        return RouteResult(kind='START_DAY', meta={'partial': True}, cleaned=cleaned, requires_wake=True, raw=raw)
# --- end micro-patch ---
# Phase C micro-patch: allow wake+start shorthand
    if has_wake and cmd in ('start', 'start day'):
        return RouteResult(kind='START_DAY', meta={'shorthand': True}, cleaned=cleaned, requires_wake=True, raw=raw)
    # Start day (now robust to punctuation)
    if cmd in ("start my day", "begin my day", "todays rundown", "today's rundown", "start the day"):
        return RouteResult(kind="START_DAY", meta={}, cleaned=cleaned, requires_wake=True, raw=raw)

    # Web lookup (robust)
    if cleaned.startswith(("search the web for ", "find the latest ", "look up ", "search for ")):
        q = cleaned
        for prefix in ("search the web for ", "look up ", "search for "):
            if q.startswith(prefix):
                q = q[len(prefix):]
        return RouteResult(kind="WEB_LOOKUP", meta={"query": q.strip(" .?")}, cleaned=cleaned, requires_wake=True, raw=raw)

    # Global media controls
    if cmd in ("pause", "resume", "play", "next", "previous", "skip", "stop"):
        cmd_map = {"pause": "pause", "resume": "resume", "play": "resume", "next": "next", "skip": "next", "previous": "previous", "stop": "pause"}
        return RouteResult(kind="SPOTIFY", meta={"cmd": cmd_map[cmd]}, cleaned=cleaned, requires_wake=True, raw=raw)

    # Spotify classifier (feed stripped so wake doesn't pollute)
    sp = classify_spotify(stripped)
    if sp and getattr(sp, "handled", False):
        meta = {"cmd": sp.cmd}
        if getattr(sp, "query", None):
            meta["query"] = sp.query
        return RouteResult(kind="SPOTIFY", meta=meta, cleaned=cleaned, requires_wake=True, raw=raw)

    return RouteResult(kind="LLM_FALLBACK", meta={}, cleaned=cleaned, requires_wake=True, raw=raw)
