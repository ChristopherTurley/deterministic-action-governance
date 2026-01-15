from __future__ import annotations

import copy

from v2.engine_adapter import EngineInput, run_engine_via_v1
from v2.contract import to_contract_output
from v2.state_reducer import reduce_pds


def _next_state(x):
    return getattr(x, 'next_state', x)


def test_m9w1_contract_attaches_context_nonbinding():
    ctx = {
        "active_app": "Safari",
        "local_date": "2026-01-10",
        "local_time": "18:33",
        "screen_hint": "Reading an article",
        "ignored_key": "should_be_dropped",
    }
    inp = EngineInput(
        raw_text="what time is it",
        awake=True,
        timestamp_utc="2026-01-10T23:33:00Z",
        context=ctx,
        pds={"awake": True},
    )
    out = run_engine_via_v1(inp)
    c = to_contract_output(out, awake_fallback=True)

    assert c.get("context_version") == "context_v1"
    cctx = c.get("context")
    assert isinstance(cctx, dict)
    assert "ignored_key" not in cctx
    assert cctx.get("active_app") == "Safari"
    assert cctx.get("local_date") == "2026-01-10"


def test_m9w1_deterministic_contract_same_input_same_output():
    ctx = {
        "active_app": "Terminal",
        "local_date": "2026-01-10",
        "local_time": "18:40",
        "screen_hint": "Running tests",
    }
    inp = EngineInput(
        raw_text="search the web for apple intelligence",
        awake=True,
        timestamp_utc="2026-01-10T23:40:00Z",
        context=ctx,
        pds={"awake": True},
    )

    out1 = run_engine_via_v1(inp)
    out2 = run_engine_via_v1(inp)

    c1 = to_contract_output(out1, awake_fallback=True)
    c2 = to_contract_output(out2, awake_fallback=True)
    assert c1 == c2


def test_m9w1_context_does_not_create_actions():
    base = EngineInput(
        raw_text="what time is it",
        awake=True,
        timestamp_utc="2026-01-10T23:45:00Z",
        context=None,
        pds={"awake": True},
    )
    with_ctx = EngineInput(
        raw_text="what time is it",
        awake=True,
        timestamp_utc="2026-01-10T23:45:00Z",
        context={
            "active_app": "Notes",
            "local_date": "2026-01-10",
            "local_time": "18:45",
            "screen_hint": "Drafting",
        },
        pds={"awake": True},
    )

    out1 = run_engine_via_v1(base)
    out2 = run_engine_via_v1(with_ctx)

    # Actions must be identical; context is non-binding.
    assert out1.actions == out2.actions


def test_m9w1_reducer_records_active_context_metadata_only():
    pds = {"awake": True, "mode": "IDLE"}
    delta = {"awake": True, "mode": "IDLE", "active_context": {"active_app": "Safari"}}

    p1 = reduce_pds(copy.deepcopy(pds), delta)
    s1 = _next_state(p1)
    p2 = reduce_pds(copy.deepcopy(s1), delta)
    s2 = _next_state(p2)

    assert isinstance(s1, dict)
    assert s1.get("awake") is True
    assert s1.get("mode") == "IDLE"
    assert isinstance(s1.get("active_context"), dict)
    assert s1["active_context"].get("active_app") == "Safari"
    # Idempotent for same inputs
    assert s1 == s2
