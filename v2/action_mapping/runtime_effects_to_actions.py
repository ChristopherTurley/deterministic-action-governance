from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


# NOTE:
# - This module MUST stay pure: mapping only.
# - No I/O, no PDS writes, no runtime calls.
# - Deterministic transforms only.


@dataclass(frozen=True)
class ObservedRuntimeEffect:
    """
    Normalized observation produced by the v2 adapter from v1 inspection-only outputs.
    Keep this small and explicit so mapping stays deterministic.
    """
    route_kind: str
    payload: Dict[str, Any]


def map_effects_to_actions(effects: List[ObservedRuntimeEffect]) -> List[Dict[str, Any]]:
    """
    Returns v2 action declarations as dicts that match your existing v2 action schema.

    Contract:
    - Every meaningful effect must yield an action.
    - No action returned here should cause side effects on its own.
    """
    actions: List[Dict[str, Any]] = []

    for eff in effects:
        k = (eff.route_kind or "").strip().upper()
        p = eff.payload or {}

        # WEB LOOKUP
        if k == "WEB_LOOKUP":
            q = str(p.get("query") or "").strip()
            actions.append({
                "type": "WEB_LOOKUP_QUERY",
                "query": q,
            })
            continue

        # OPEN LINK
        if k == "OPEN_LINK":
            idx = p.get("index")
            actions.append({
                "type": "OPEN_LINK_INDEX",
                "index": idx,
            })
            continue

        # SPOTIFY
        if k == "SPOTIFY":
            cmd = str(p.get("command") or "").strip()
            actions.append({
                "type": "SPOTIFY_COMMAND",
                "command": cmd,
            })
            continue

        # TIME (read-only but still must be an action)
        if k == "TIME":
            actions.append({
                "type": "TIME_READ",
            })
            continue

        # PRIORITY
        if k == "PRIORITY_GET":
            actions.append({
                "type": "PRIORITY_GET",
            })
            continue

        if k == "PRIORITY_SET":
            actions.append({
                "type": "PRIORITY_SET",
                "item": p.get("item"),
                "priority": p.get("priority"),
            })
            continue

        # START DAY -> intake
        if k == "START_DAY":
            actions.append({
                "type": "ENTER_TASK_INTAKE",
            })
            continue

        # WAKE / SLEEP -> explicit awake state set
        if k == "WAKE":
            actions.append({
                "type": "STATE_SET_AWAKE",
                "awake": True,
            })
            continue

        if k == "SLEEP":
            actions.append({
                "type": "STATE_SET_AWAKE",
                "awake": False,
            })
            continue

        # If you support other kinds already, extend here explicitly.
        # Fail-closed: unknown kinds produce NO actions unless you whitelist them.
        # That preserves determinism and prevents accidental side effects.
        #
        # IMPORTANT: If a new kind causes a meaningful effect, you MUST add a mapping.
        # Unknown kinds should be caught by a completeness test.
        pass

    return actions
