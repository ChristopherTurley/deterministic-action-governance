from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(frozen=True)
class RouteResult:
    """
    Canonical router output shape. All routing functions must return this.
    """
    kind: str
    cleaned: str
    raw: str
    meta: Dict[str, Any] = field(default_factory=dict)

    # Helpful debug/state fields (optional but used by core.py + harness)
    has_wake: bool = False
    requires_wake: bool = False
