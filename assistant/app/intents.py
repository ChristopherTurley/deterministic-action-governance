from __future__ import annotations

import re
from typing import List


OPEN_LINK_TRIGGERS: List[str] = [
    "open it",
    "open that",
    "open the link",
    "open link",
    "show me",
    "pull it up",
    "pull that up",
    "bring it up",
    "take me there",
]


def normalize_text(t: str) -> str:
    t = (t or "").strip().lower()
    t = re.sub(r"\s+", " ", t)
    return t


def wants_open_link(text: str) -> bool:
    t = normalize_text(text)
    return any(p in t for p in OPEN_LINK_TRIGGERS)
