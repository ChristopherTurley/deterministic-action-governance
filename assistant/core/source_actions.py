from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

OPEN_SOURCE_PAT = re.compile(r"\bopen\s+(?:source|link)\s+(\d+)\b", re.I)
SHOW_SOURCES_PAT = re.compile(r"\b(show|list)\s+sources\b", re.I)

def parse_open_source(text: str) -> Optional[int]:
    m = OPEN_SOURCE_PAT.search(text or "")
    if not m:
        return None
    try:
        return int(m.group(1))
    except Exception:
        return None

def wants_show_sources(text: str) -> bool:
    return bool(SHOW_SOURCES_PAT.search(text or ""))

def build_sources_display(last_sources: List[Dict[str, Any]]) -> List[str]:
    if not last_sources:
        return ["No saved sources from the last request."]
    out = ["Sources:"]
    for i, s in enumerate(last_sources, start=1):
        out.append(f"{i}. {s.get('title','Source')}")
    out.append("Say: open source 1")
    return out
