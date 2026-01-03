from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class VeraState:
    awake: bool = True
    top_priority: Optional[str] = None
    last_web: List[Dict[str, Any]] = field(default_factory=list)


class StateStore:
    def __init__(self) -> None:
        self.state = VeraState()

    def set_priority(self, value: str) -> None:
        v = (value or "").strip()
        self.state.top_priority = v if v else None

    def get_priority(self) -> Optional[str]:
        return self.state.top_priority

    def set_last_web(self, items: List[Dict[str, Any]]) -> None:
        self.state.last_web = items[:10]

    def get_last_web(self) -> List[Dict[str, Any]]:
        return list(self.state.last_web or [])

    def sleep(self) -> None:
        self.state.awake = False

    def wake(self) -> None:
        self.state.awake = True
