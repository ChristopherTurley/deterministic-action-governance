from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AppState:
    """
    Central state container so main.py doesn’t become a god-object.
    This is intentionally minimal for now.
    """
    awake: bool = False
    last_web_query: str = ""
    last_web_sources: List[Dict[str, Any]] = field(default_factory=list)
