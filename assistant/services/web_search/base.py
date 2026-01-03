from __future__ import annotations

from dataclasses import dataclass


@dataclass
class WebSource:
    title: str
    url: str
    snippet: str = ""
    source: str = "unknown"

