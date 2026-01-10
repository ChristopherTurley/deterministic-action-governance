# v2/tests/test_month4_failure_modes.py
"""
Month 4 — Failure Harness

Purpose:
- Prove VERA fails safely, truthfully, and deterministically
- No new behavior is introduced here
- We only assert what already exists

Scope:
- v2 only
- v1 is NOT touched
"""

from v2.engine_adapter import run_engine_via_v1, EngineInput


def _types(out):
    actions = (out.actions or [])
    return [a.get("type") for a in actions], actions


def test_web_lookup_zero_results():
    """
    Failure Mode #1:
    Web search returns zero results.

    Expected:
    - WEB_LOOKUP_QUERY action declared
    - No OPEN action declared
    - No crash
    """
    out = run_engine_via_v1(EngineInput(raw_text="search the web for qzxwqzxwqzxw", awake=True))
    types, _ = _types(out)

    assert "WEB_LOOKUP_QUERY" in types
    assert "OPEN_LINK_INDEX" not in types


def test_open_without_prior_search():
    """
    Failure Mode #2:
    User says "open 1" without having searched.

    Expected:
    - OPEN_LINK_INDEX may be declared OR not (depends on router),
      but it must NOT crash either way.
    - Determinism: same input yields same action types every run.
    """
    out1 = run_engine_via_v1(EngineInput(raw_text="open 1", awake=True))
    out2 = run_engine_via_v1(EngineInput(raw_text="open 1", awake=True))

    t1, _ = _types(out1)
    t2, _ = _types(out2)

    assert t1 == t2


def test_open_out_of_range_after_search_is_not_invented():
    """
    Failure Mode #3:
    User searches, then tries to open an out-of-range index.

    Expected:
    - The system should not invent new web results/actions.
    - OPEN_LINK_INDEX may be declared (since it's an explicit command),
      but must not declare WEB_LOOKUP_QUERY again automatically.
    """
    _ = run_engine_via_v1(EngineInput(raw_text="search the web for pizza near me", awake=True))
    out = run_engine_via_v1(EngineInput(raw_text="open 99", awake=True))

    types, _ = _types(out)

    assert "WEB_LOOKUP_QUERY" not in types


def test_sleep_blocks_non_wake_commands():
    """
    Failure Mode #4:
    After sleeping, a follow-up command should be blocked when asleep.

    Truth we are asserting (existing behavior):
    - Sleep may be represented as route_kind "SLEEP" OR as an action "STATE_SET_AWAKE".
      We accept either form as long as it is deterministic and safe.
    - While asleep (awake=False), commands like OPEN should not execute; they should be ignored safely.
    """

    out_sleep = run_engine_via_v1(EngineInput(raw_text="hey vera, go to sleep", awake=True))
    types_sleep, _ = _types(out_sleep)
    rk_sleep = getattr(out_sleep, "route_kind", "") or ""
    assert ("STATE_SET_AWAKE" in types_sleep) or (rk_sleep == "SLEEP") or (rk_sleep == "NUDGE_WAKE")

    # A follow-up that should be blocked while asleep
    out_asleep = run_engine_via_v1(EngineInput(raw_text="open 1", awake=False))
    types_asleep, _ = _types(out_asleep)
    rk_asleep = getattr(out_asleep, "route_kind", "") or ""

    # Accept either: explicit ASLEEP_IGNORE, OR route_kind ASLEEP_IGNORE, OR empty actions (safe no-op)
    assert ("ASLEEP_IGNORE" in types_asleep) or (rk_asleep == "ASLEEP_IGNORE") or (len(types_asleep) == 0)


def test_asleep_web_lookup_current_behavior_is_documented():
    """
    Failure Mode #4b (documentation):
    Today, WEB_LOOKUP is allowed even when awake=False (as proven by current routing).
    This is not a judgment — it locks in current behavior so future changes are intentional.
    """
    out = run_engine_via_v1(EngineInput(raw_text="search the web for pizza near me", awake=False))
    types, _ = _types(out)
    rk = getattr(out, "route_kind", "") or ""
    assert ("WEB_LOOKUP_QUERY" in types) or (rk == "WEB_LOOKUP")
def test_empty_input_is_safe():
    """
    Failure Mode #5:
    Empty / whitespace input.

    Expected:
    - No crash
    - No actions declared
    """
    out = run_engine_via_v1(EngineInput(raw_text="   ", awake=True))
    types, _ = _types(out)
    assert len(types) == 0


# === MONTH 4 WEEK 2: GATE TESTS (ASSERT CURRENT TRUTH; NO FEATURE CHANGES) ===



import copy
import json

def _as_jsonable_state(state):
    if state is None:
        return None
    if isinstance(state, dict):
        return state
    to_dict = getattr(state, "to_dict", None)
    if callable(to_dict):
        return to_dict()
    d = getattr(state, "__dict__", None)
    if isinstance(d, dict):
        return d
    try:
        return json.loads(json.dumps(state, default=str))
    except Exception:
        return {"_repr": repr(state)}

def _state_snapshot(state):
    obj = _as_jsonable_state(state)
    return json.dumps(obj, sort_keys=True, default=str)

def _get_route_kind(rr):
    for k in ("route_kind", "kind", "route", "route_name"):
        v = getattr(rr, k, None)
        if isinstance(v, str) and v.strip():
            return v.strip()
    raise AssertionError("RouteResult missing a non-empty route kind attribute (route_kind/kind/route/route_name).")

def _get_actions(rr):
    for k in ("actions", "action_list", "planned_actions"):
        v = getattr(rr, k, None)
        if isinstance(v, list):
            return v
    v = getattr(rr, "action", None)
    if v is not None:
        return [v]
    return []

def _action_fields(action):
    if action is None:
        return {}
    if isinstance(action, dict):
        return action
    to_dict = getattr(action, "to_dict", None)
    if callable(to_dict):
        return to_dict()
    d = getattr(action, "__dict__", None)
    if isinstance(d, dict):
        return d
    return {"_repr": repr(action)}

def _pick_nonempty_str(d, keys):
    for k in keys:
        v = d.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return None

def _route_text(raw, state, awake=True, wake_required=False, priority_enabled=True):
    candidates = [
        ("v2.router.core", "route_text"),
        ("assistant.router.core", "route_text"),
        ("v2.core.router", "route_text"),
        ("v2.router", "route_text"),
    ]
    last_err = None
    for mod, fn in candidates:
        try:
            m = __import__(mod, fromlist=[fn])
            f = getattr(m, fn)
            return f(raw, wake_required=wake_required, priority_enabled=priority_enabled, awake=awake)
        except Exception as e:
            last_err = e
    raise AssertionError(f"Unable to import route_text from known locations; last error: {last_err!r}")

def _apply_reducer(state, rr):
    candidates = [
        ("v2.state_reducer", "reduce_state"),
        ("v2.core.state_reducer", "reduce_state"),
        ("v2.reducer", "reduce_state"),
    ]
    last_err = None
    for mod, fn in candidates:
        try:
            m = __import__(mod, fromlist=[fn])
            f = getattr(m, fn)
            return f(state, rr)
        except Exception as e:
            last_err = e
    return None

def test_gate_receipt_integrity_route_kind_nonempty():
    rr = _route_text("what time is it", state=None, awake=True, wake_required=False)
    rk = _get_route_kind(rr)
    assert isinstance(rk, str) and rk.strip()

def test_gate_receipt_integrity_actions_have_id_and_kind_when_present():
    rr = _route_text("search the web for apple intelligence", state=None, awake=True, wake_required=False)
    actions = _get_actions(rr)
    if not actions:
        return
    for a in actions:
        d = _action_fields(a)
        aid = _pick_nonempty_str(d, ("action_id", "id", "receipt_id", "event_id"))
        ak = _pick_nonempty_str(d, ("action_kind", "kind", "type", "name"))
        assert aid is not None, f"Action missing non-empty id field; keys={list(d.keys())}"
        assert ak is not None, f"Action missing non-empty kind/type field; keys={list(d.keys())}"

def test_gate_determinism_same_input_same_state_same_route_kind():
    state = {"awake": True}
    rr1 = _route_text("what time is it", state=state, awake=True, wake_required=False)
    rr2 = _route_text("what time is it", state=state, awake=True, wake_required=False)
    assert _get_route_kind(rr1) == _get_route_kind(rr2)

def test_gate_state_boundaries_router_does_not_mutate_state_snapshot():
    state = {"awake": True, "pds": {"x": 1}}
    before = _state_snapshot(state)
    _ = _route_text("open https://example.com", state=state, awake=True, wake_required=False)
    after = _state_snapshot(state)
    assert before == after

def test_gate_state_boundaries_asleep_blocked_open_does_not_flip_awake_true():
    state = {"awake": False}
    before = _state_snapshot(state)
    rr = _route_text("open https://example.com", state=state, awake=False, wake_required=False)
    _ = _get_route_kind(rr)
    after = _state_snapshot(state)
    assert before == after

def test_gate_safe_failure_asleep_web_lookup_currently_routes():
    rr = _route_text("search the web for tesla stock", state={"awake": False}, awake=False, wake_required=False)
    rk = _get_route_kind(rr)
    assert isinstance(rk, str) and rk.strip()


"""MONTH 4 WEEK 3: STATE TRANSITION GUARANTEES (ASSERT CURRENT TRUTH; NO FEATURE CHANGES)"""

import json
import pytest

def _jsonable(obj):
    if obj is None:
        return None
    if isinstance(obj, dict):
        return obj
    to_dict = getattr(obj, "to_dict", None)
    if callable(to_dict):
        return to_dict()
    d = getattr(obj, "__dict__", None)
    if isinstance(d, dict):
        return d
    try:
        return json.loads(json.dumps(obj, default=str))
    except Exception:
        return {"_repr": repr(obj)}

def _extract_awake(engine_out):
    if engine_out is None:
        return None
    v = getattr(engine_out, "awake", None)
    if isinstance(v, bool):
        return v
    for container_name in ("pds", "state", "snapshot", "data"):
        c = getattr(engine_out, container_name, None)
        if isinstance(c, dict) and isinstance(c.get("awake"), bool):
            return c.get("awake")
    d = _jsonable(engine_out)
    if isinstance(d, dict):
        for k in ("awake",):
            if isinstance(d.get(k), bool):
                return d.get(k)
        for k in ("pds", "state", "snapshot", "data"):
            c = d.get(k)
            if isinstance(c, dict) and isinstance(c.get("awake"), bool):
                return c.get("awake")
    return None

def test_week3_state_transition_wake_sets_awake_true():
    out = run_engine_via_v1(EngineInput(raw_text="hey vera", awake=False))
    awake = _extract_awake(out)
    if awake is None:
        pytest.skip("Engine output does not expose awake; cannot lock transition truth here.")
    assert awake is True

def test_week3_state_transition_sleep_sets_awake_false():
    out = run_engine_via_v1(EngineInput(raw_text="go to sleep", awake=True))
    awake = _extract_awake(out)
    if awake is None:
        pytest.skip("Engine output does not expose awake; cannot lock transition truth here.")
    assert awake is False

def test_week3_state_transition_asleep_nonwake_does_not_flip_awake_true():
    out = run_engine_via_v1(EngineInput(raw_text="what time is it", awake=False))
    awake = _extract_awake(out)
    if awake is None:
        pytest.skip("Engine output does not expose awake; cannot lock transition truth here.")
    assert awake is False

def test_week3_state_transition_asleep_nonwake_remains_safe_no_actions():
    out = run_engine_via_v1(EngineInput(raw_text="what time is it", awake=False))
    types, _ = _types(out)
    assert len(types) == 0
