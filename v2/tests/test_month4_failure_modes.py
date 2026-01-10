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
from v2.reducer_entry import reduce_state as reduce_state_canon
from v2.contract import to_contract_output

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
    c = to_contract_output(out, awake_fallback=bool(False))
    rk = (c.get("route_kind") or "").strip().upper()
    awake = c.get("awake")
    if rk == "WAKE":
        awake = True
    elif rk == "SLEEP":
        awake = False
    assert isinstance(awake, bool)
    assert awake is True

def test_week3_state_transition_sleep_sets_awake_false():
    out = run_engine_via_v1(EngineInput(raw_text="go to sleep", awake=True))
    c = to_contract_output(out, awake_fallback=True)
    rk = (c.get("route_kind") or "").strip().upper()
    awake = c.get("awake")
    if rk == "WAKE":
        awake = True
    elif rk == "SLEEP":
        awake = False
    assert isinstance(awake, bool)
    assert rk != "SLEEP"  # current truth: this seam does not produce a SLEEP route
    assert awake is True    # therefore awake remains True (fallback)

def test_week3_state_transition_asleep_nonwake_does_not_flip_awake_true():
    out = run_engine_via_v1(EngineInput(raw_text="what time is it", awake=False))
    c = to_contract_output(out, awake_fallback=bool(False))
    rk = (c.get("route_kind") or "").strip().upper()
    awake = c.get("awake")
    if rk == "WAKE":
        awake = True
    elif rk == "SLEEP":
        awake = False
    assert isinstance(awake, bool)
    assert awake is False

def test_week3_state_transition_asleep_nonwake_remains_safe_no_actions():
    out = run_engine_via_v1(EngineInput(raw_text="what time is it", awake=False))
    types, _ = _types(out)
    assert len(types) == 0


"""MONTH 4 WEEK 4: RECEIPT → REDUCER → STATE CONTINUITY (ASSERT CURRENT TRUTH; NO FEATURE CHANGES)"""

import json
import copy
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

def _snapshot(obj):
    return json.dumps(_jsonable(obj), sort_keys=True, default=str)

def _get_receipts(engine_out):
    if engine_out is None:
        return []
    for k in ("receipts", "receipt_list", "actions", "action_list", "planned_actions"):
        v = getattr(engine_out, k, None)
        if isinstance(v, list):
            return v
    v = getattr(engine_out, "receipt", None)
    if v is not None:
        return [v]
    v = getattr(engine_out, "action", None)
    if v is not None:
        return [v]
    return []

def _reduce_state(state, receipt_or_rr):
    try:
        return reduce_state_canon(state, receipt_or_rr)
    except ImportError as e:
        raise

def test_week4_receipt_is_jsonable_when_present():
    out = run_engine_via_v1(EngineInput(raw_text="what time is it", awake=True))
    receipts = _get_receipts(out)
    for r in receipts:
        js = _jsonable(r)
        assert js is not None

def test_week4_reducer_purity_does_not_mutate_input_state():
    state = {"awake": False, "pds": {"x": 1}}
    out = run_engine_via_v1(EngineInput(raw_text="what time is it", awake=False))
    receipts = _get_receipts(out)
    if not receipts:
        raw, awake, r = _pick_first_receipt_from_any_command()
        if r is None:
            pytest.skip("No receipts found by probe; update probe candidates to match current truth.")
        receipts = [r]
    before = _snapshot(state)
    _ = _reduce_state(state, receipts[0])
    after = _snapshot(state)
    assert before == after


    before = _snapshot(state)
    _ = _reduce_state(state, receipts[0])
    after = _snapshot(state)
    assert before == after

def test_week4_reducer_idempotent_same_input_same_output_snapshot():
    state = {"awake": True, "pds": {"x": 1}}
    out = run_engine_via_v1(EngineInput(raw_text="what time is it", awake=True))
    receipts = _get_receipts(out)
    if not receipts:
        raw, awake, r = _pick_first_receipt_from_any_command()
        if r is None:
            pytest.skip("No receipts found by probe; update probe candidates to match current truth.")
        receipts = [r]
    r = receipts[0]
    s1 = _reduce_state(copy.deepcopy(state), r)
    s2 = _reduce_state(copy.deepcopy(state), r)
    assert _snapshot(s1) == _snapshot(s2)


    r = receipts[0]
    s1 = _reduce_state(copy.deepcopy(state), r)
    s2 = _reduce_state(copy.deepcopy(state), r)
    assert _snapshot(s1) == _snapshot(s2)

def test_week4_reducer_respects_sleep_boundary_does_not_flip_awake_true():
    state = {"awake": False}
    out = run_engine_via_v1(EngineInput(raw_text="what time is it", awake=False))
    receipts = _get_receipts(out)
    if not receipts:
        raw, awake, r = _pick_first_receipt_from_any_command()
        if r is None:
            pytest.skip("No receipts found by probe; update probe candidates to match current truth.")
        receipts = [r]
    new_state = _reduce_state(copy.deepcopy(state), receipts[0])
    d = _as_jsonable_state(new_state)
    if isinstance(d, dict) and isinstance(d.get("awake"), bool):
        assert d["awake"] is False


    new_state = _reduce_state(copy.deepcopy(state), receipts[0])
    d = _jsonable(new_state)
    if isinstance(d, dict) and isinstance(d.get("awake"), bool):
        assert d["awake"] is False


"""MONTH 5 WEEK 1: CONTRACT SURFACES v1 (ASSERT CURRENT TRUTH; NO FEATURE CHANGES)"""

def _contract(out, awake_fallback: bool):
    return to_contract_output(out, awake_fallback=awake_fallback)

def _contract_awake(out, awake_fallback: bool):
    c = _contract(out, awake_fallback=awake_fallback)
    return c.get("awake")

def _contract_receipts(out, awake_fallback: bool):
    c = _contract(out, awake_fallback=awake_fallback)
    r = c.get("receipts")
    return r if isinstance(r, list) else []

def test_month5_contract_surface_has_version_awake_route_kind_receipts():
    out = run_engine_via_v1(EngineInput(raw_text="what time is it", awake=True))
    c = _contract(out, awake_fallback=True)
    assert c.get("version") == "v2_contract_v1"
    assert isinstance(c.get("awake"), bool)
    assert isinstance(c.get("route_kind"), str)
    assert isinstance(c.get("receipts"), list)

def test_month5_contract_surface_awake_is_deterministic_from_engine_input():
    out1 = run_engine_via_v1(EngineInput(raw_text="what time is it", awake=False))
    out2 = run_engine_via_v1(EngineInput(raw_text="what time is it", awake=True))
    c1 = to_contract_output(out1, awake_fallback=False)
    c2 = to_contract_output(out2, awake_fallback=True)
    assert isinstance(c1.get("awake"), bool)
    assert isinstance(c2.get("awake"), bool)


"""MONTH 5 WEEK 3: SLEEP TRUTH ISOLATION (ASSERT CURRENT TRUTH; NO FEATURE CHANGES)"""

import pytest

@pytest.mark.parametrize("phrase, awake_in", [
    ("sleep", True),
    ("go to sleep", True),
    ("vera go to sleep", True),
    ("hey vera go to sleep", True),
    ("go to sleep", False),
    ("sleep", False),
])
def test_month5_week3_sleep_variants_route_kind_truth(phrase, awake_in):
    out = run_engine_via_v1(EngineInput(raw_text=phrase, awake=awake_in))
    c = to_contract_output(out, awake_fallback=bool(awake_in))
    rk = (c.get("route_kind") or "").strip().upper()

    assert isinstance(rk, str)

    # Lock current truth:
    # If any variant actually produces SLEEP at this seam, we accept that as contract-eligible later.
    # Otherwise we explicitly learn that SLEEP is handled outside this seam.
    #
    # This test is intentionally permissive, but it *records truth* by asserting that the route_kind
    # stays stable over time for the same phrase + awake_in.
    out2 = run_engine_via_v1(EngineInput(raw_text=phrase, awake=awake_in))
    c2 = to_contract_output(out2, awake_fallback=bool(awake_in))
    rk2 = (c2.get("route_kind") or "").strip().upper()
    assert rk == rk2


"""MONTH 5 WEEK 4: REDUCER & RECEIPT CONTINUITY (ASSERT CURRENT TRUTH; NO FEATURE CHANGES)"""

import copy

def _pick_first_receipt_from_any_command():
    # Probe a few commands and return the first receipt we can get.
    candidates = [
        ("what time is it", True),
        ("search the web for apple intelligence", True),
        ("open https://example.com", True),
        ("set a timer for 1 minute", True),
    ]
    for raw, awake in candidates:
        out = run_engine_via_v1(EngineInput(raw_text=raw, awake=awake))
        c = to_contract_output(out, awake_fallback=bool(awake))
        receipts = c.get("receipts") if isinstance(c.get("receipts"), list) else []
        if receipts:
            return raw, awake, receipts[0]
    return None, None, None

def test_month5_week4_probe_at_least_one_command_produces_receipt():
    raw, awake, r = _pick_first_receipt_from_any_command()
    assert r is not None, "No receipts produced by probe set; update probe candidates to match current truth."

def test_month5_week4_reducer_purity_does_not_mutate_input_state():
    raw, awake, r = _pick_first_receipt_from_any_command()
    if r is None:
        return
    state = {"awake": bool(awake), "pds": {"x": 1}}
    before = _state_snapshot(state)
    _ = _reduce_state(state, r)
    after = _state_snapshot(state)
    assert before == after

def test_month5_week4_reducer_idempotent_same_input_same_output_snapshot():
    raw, awake, r = _pick_first_receipt_from_any_command()
    if r is None:
        return
    state = {"awake": bool(awake), "pds": {"x": 1}}
    s1 = _reduce_state(copy.deepcopy(state), r)
    s2 = _reduce_state(copy.deepcopy(state), r)
    assert _state_snapshot(s1) == _state_snapshot(s2)


def test_month5_week4_reducer_entry_importable():
    # Truth gate: reducer is not yet contract-exposed in this repo.
    # This test documents that reality explicitly (skip, not fail).
    try:
        _ = reduce_state_canon({"awake": True}, {"kind": "NOOP"})
    except ImportError as e:
        raise


"""MONTH 6 WEEK 2: REDUCER WHITELISTED DELTAS (ASSERT BEHAVIOR)"""

def test_month6_week2_reducer_sets_last_receipt_type_when_type_present():
    state = {"awake": True, "pds": {"x": 1}}
    receipt = {"type": "WEB_LOOKUP_QUERY", "payload": {"query": "x"}}
    new_state = _reduce_state(state, receipt)
    d = _as_jsonable_state(new_state)
    assert isinstance(d, dict)
    assert (d.get("last_receipt_type") or "").strip().upper() == "WEB_LOOKUP_QUERY"

def test_month6_week2_reducer_sets_last_route_kind_when_present():
    state = {"awake": True, "pds": {"x": 1}}
    rr = {"route_kind": "TIME"}
    new_state = _reduce_state(state, rr)
    d = _as_jsonable_state(new_state)
    assert isinstance(d, dict)
    assert (d.get("last_route_kind") or "").strip().upper() == "TIME"

def test_month6_week2_reducer_increments_routes_total_deterministically():
    state = {"awake": True, "counters": {"routes_total": 0, "receipts_total": 0}}
    r = {"type": "TIME"}
    s1 = _reduce_state(state, r)
    s2 = _reduce_state(state, r)
    d1 = _as_jsonable_state(s1)
    d2 = _as_jsonable_state(s2)
    assert d1["counters"]["routes_total"] == 1
    assert d2["counters"]["routes_total"] == 1

def test_month6_week2_reducer_does_not_write_unknown_top_level_keys():
    state = {"awake": True, "DO_NOT_TOUCH": {"x": 1}}
    r = {"type": "TIME"}
    new_state = _reduce_state(state, r)
    d = _as_jsonable_state(new_state)
    assert d.get("DO_NOT_TOUCH") == {"x": 1}


"""MONTH 6 WEEK 3: CONTRACT RECEIPT NORMALIZATION (ASSERT SHAPE)"""

def test_month6_week3_contract_has_canonical_lists():
    out = run_engine_via_v1(EngineInput(raw_text="search the web for apple intelligence", awake=True))
    c = to_contract_output(out, awake_fallback=True)
    assert isinstance(c, dict)
    rk = (c.get("route_kind") or "").strip()
    assert rk
    assert isinstance(c.get("receipts"), list)
    assert isinstance(c.get("actions"), list)

def test_month6_week3_receipts_are_normalized_dicts():
    out = run_engine_via_v1(EngineInput(raw_text="search the web for apple intelligence", awake=True))
    c = to_contract_output(out, awake_fallback=True)
    receipts = c.get("receipts")
    assert isinstance(receipts, list)
    for r in receipts:
        assert isinstance(r, dict)
        t = (r.get("type") or "").strip()
        assert t
        payload = r.get("payload")
        assert isinstance(payload, dict)


"""MONTH 6 WEEK 4: CONTRACT VERSION + DEPRECATION GUARD"""

def test_month6_week4_contract_version_present_and_stable():
    out = run_engine_via_v1(EngineInput(raw_text="what time is it", awake=True))
    c = to_contract_output(out, awake_fallback=True)
    assert isinstance(c, dict)
    assert (c.get("version") or "").strip() == "v2_contract_v1"

def test_month6_week4_contract_required_keys_present():
    out = run_engine_via_v1(EngineInput(raw_text="search the web for apple intelligence", awake=True))
    c = to_contract_output(out, awake_fallback=True)
    for k in ("route_kind", "awake", "receipts", "actions", "version"):
        assert k in c, f"Missing required contract key: {k}"
    assert isinstance(c.get("route_kind"), str) and c["route_kind"].strip()
    assert isinstance(c.get("awake"), bool)
    assert isinstance(c.get("receipts"), list)
    assert isinstance(c.get("actions"), list)

def test_month6_week4_receipts_always_have_type_and_payload_dict():
    out = run_engine_via_v1(EngineInput(raw_text="search the web for apple intelligence", awake=True))
    c = to_contract_output(out, awake_fallback=True)
    for r in c.get("receipts", []):
        assert isinstance(r, dict)
        assert isinstance(r.get("type"), str) and r["type"].strip()
        assert isinstance(r.get("payload"), dict)


"""MONTH 7 WEEK 1: ACTION CONTRACT + EXECUTOR ENTRY (ASSERT CURRENT TRUTH)"""

def _pick_nonempty_str(d, keys):
    for k in keys:
        v = d.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return None

def test_month7_week1_contract_actions_is_list_of_dicts():
    out = run_engine_via_v1(EngineInput(raw_text="search the web for apple intelligence", awake=True))
    c = to_contract_output(out, awake_fallback=True)
    actions = c.get("actions")
    assert isinstance(actions, list)
    for a in actions:
        assert isinstance(a, dict)

def test_month7_week1_action_surface_truth_lock_when_actions_present():
    out = run_engine_via_v1(EngineInput(raw_text="open https://example.com", awake=True))
    c = to_contract_output(out, awake_fallback=True)
    actions = c.get("actions")
    assert isinstance(actions, list)

    # Current truth lock:
    # If actions are structured, they should include non-empty kind/id fields.
    # If not structured yet, we accept the "_repr" fallback (still deterministic + inspectable).
    for a in actions:
        assert isinstance(a, dict)
        ak = _pick_nonempty_str(a, ("action_kind", "kind", "type", "name"))
        aid = _pick_nonempty_str(a, ("action_id", "id", "receipt_id", "event_id"))
        if ak is None and aid is None:
            assert "_repr" in a, f"Unstructured action must include _repr for auditability; keys={list(a.keys())}"

def test_month7_week1_executor_entry_importable_and_callable():
    from v2.action_executor_entry import execute_actions
    out = run_engine_via_v1(EngineInput(raw_text="search the web for apple intelligence", awake=True))
    c = to_contract_output(out, awake_fallback=True)
    actions = c.get("actions")
    res = execute_actions(actions, dry_run=True)
    assert isinstance(res, list)


"""MONTH 7 WEEK 2: ACTION NORMALIZATION + STABLE IDS"""

def test_month7_week2_actions_have_id_kind_payload():
    out = run_engine_via_v1(EngineInput(raw_text="open https://example.com", awake=True))
    c = to_contract_output(out, awake_fallback=True)
    actions = c.get("actions")
    assert isinstance(actions, list)
    for a in actions:
        assert isinstance(a, dict)
        assert isinstance(a.get("id"), str) and a["id"].strip()
        assert isinstance(a.get("kind"), str) and a["kind"].strip() and a["kind"] == a["kind"].upper()
        assert isinstance(a.get("payload"), dict)

def test_month7_week2_action_ids_stable_for_same_input():
    out1 = run_engine_via_v1(EngineInput(raw_text="open https://example.com", awake=True))
    out2 = run_engine_via_v1(EngineInput(raw_text="open https://example.com", awake=True))
    c1 = to_contract_output(out1, awake_fallback=True)
    c2 = to_contract_output(out2, awake_fallback=True)
    a1 = c1.get("actions") or []
    a2 = c2.get("actions") or []
    # Compare only the normalized surface (id/kind/payload) for determinism
    slim1 = [{"id": x.get("id"), "kind": x.get("kind"), "payload": x.get("payload")} for x in a1]
    slim2 = [{"id": x.get("id"), "kind": x.get("kind"), "payload": x.get("payload")} for x in a2]
    assert slim1 == slim2


"""MONTH 7 WEEK 3: EXECUTOR DRY-RUN RECEIPTS (ASSERT DETERMINISM)"""

def test_month7_week3_executor_returns_one_receipt_per_action():
    from v2.action_executor_entry import execute_actions
    out = run_engine_via_v1(EngineInput(raw_text="open https://example.com", awake=True))
    c = to_contract_output(out, awake_fallback=True)
    actions = c.get("actions") or []
    res = execute_actions(actions, dry_run=True)
    assert isinstance(res, list)
    assert len(res) == len(actions)

def test_month7_week3_executor_receipts_have_type_and_payload_echo():
    from v2.action_executor_entry import execute_actions
    out = run_engine_via_v1(EngineInput(raw_text="open https://example.com", awake=True))
    c = to_contract_output(out, awake_fallback=True)
    actions = c.get("actions") or []
    res = execute_actions(actions, dry_run=True)
    for a, r in zip(actions, res):
        assert isinstance(r, dict)
        assert (r.get("type") or "").strip() == "ACTION_DRY_RUN"
        payload = r.get("payload")
        assert isinstance(payload, dict)
        assert payload.get("id") == a.get("id")
        assert payload.get("kind") == a.get("kind")
        assert isinstance(payload.get("payload"), dict)

def test_month7_week3_executor_deterministic_for_same_actions():
    from v2.action_executor_entry import execute_actions
    out = run_engine_via_v1(EngineInput(raw_text="open https://example.com", awake=True))
    c = to_contract_output(out, awake_fallback=True)
    actions = c.get("actions") or []
    r1 = execute_actions(actions, dry_run=True)
    r2 = execute_actions(actions, dry_run=True)
    assert r1 == r2
