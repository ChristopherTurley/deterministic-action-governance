from __future__ import annotations

from v2.action_mapping.runtime_effects_to_actions import ObservedRuntimeEffect, map_effects_to_actions


REQUIRED_ROUTE_KINDS = [
    "WEB_LOOKUP",
    "OPEN_LINK",
    "SPOTIFY",
    "TIME",
    "PRIORITY_GET",
    "PRIORITY_SET",
    "START_DAY",
    "WAKE",
    "SLEEP",
]


def test_required_route_kinds_map_to_actions():
    for kind in REQUIRED_ROUTE_KINDS:
        eff = ObservedRuntimeEffect(route_kind=kind, payload={"query": "x", "index": 1, "command": "play", "item": "a", "priority": 1})
        actions = map_effects_to_actions([eff])

        assert isinstance(actions, list)
        assert len(actions) == 1, f"{kind} did not map to exactly one action; got {actions}"

        action_type = actions[0].get("type")
        assert action_type, f"{kind} produced action without type: {actions[0]}"


def test_wake_sleep_are_explicit_state_set_awake():
    wake = map_effects_to_actions([ObservedRuntimeEffect("WAKE", {})])[0]
    sleep = map_effects_to_actions([ObservedRuntimeEffect("SLEEP", {})])[0]

    assert wake["type"] == "STATE_SET_AWAKE"
    assert wake["awake"] is True

    assert sleep["type"] == "STATE_SET_AWAKE"
    assert sleep["awake"] is False
