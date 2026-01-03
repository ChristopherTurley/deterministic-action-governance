from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List

from assistant.actions.browser import open_url


@dataclass
class ActionResult:
    did_action: bool
    spoken_confirmation: str = ""
    opened_url: str = ""


def _normalize(t: str) -> str:
    t = (t or "").strip().lower()
    t = re.sub(r"\s+", " ", t)
    return t


def _wants_open_or_play(user_text: str) -> bool:
    t = _normalize(user_text)
    triggers = [
        "open", "play", "start", "launch",
        "search and play", "find and play", "open and play",
    ]
    return any(x in t for x in triggers)


def choose_best_url(web_sources: List[dict]) -> str:
    if not web_sources:
        return ""
    return (web_sources[0].get("url") or "").strip()


def maybe_execute_actions(user_text: str, web_sources: List[dict]) -> ActionResult:
    if not _wants_open_or_play(user_text):
        return ActionResult(did_action=False)

    url = choose_best_url(web_sources)
    if not url:
        return ActionResult(did_action=False, spoken_confirmation="I couldn't find a link to open.")

    ok = open_url(url)
    if ok:
        return ActionResult(did_action=True, spoken_confirmation="Opening it now.", opened_url=url)

    return ActionResult(did_action=False, spoken_confirmation="I tried to open it but something blocked the browser.")
