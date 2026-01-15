from __future__ import annotations

from v2.engine_adapter import EngineInput, run_engine_via_v1
from v2.contract import to_contract_output


def test_m9w2_contract_attaches_suggestions_version_and_list():
    inp = EngineInput(
        raw_text="what time is it",
        awake=True,
        timestamp_utc="2026-01-10T23:50:00Z",
        context={"active_app": "Safari", "local_date": "2026-01-10", "local_time": "18:50", "screen_hint": "Reading"},
        pds={"awake": True},
    )
    out = run_engine_via_v1(inp)
    c = to_contract_output(out, awake_fallback=True)

    assert c.get("suggestions_version") == "suggestions_v1"
    sug = c.get("suggestions")
    assert isinstance(sug, list)
    if sug:
        assert isinstance(sug[0], dict)
        assert "label" in sug[0]
        assert "reason" in sug[0]


def test_m9w2_suggestions_are_deterministic_for_same_input():
    ctx = {"active_app": "Safari", "local_date": "2026-01-10", "local_time": "18:55", "screen_hint": "Article"}
    inp = EngineInput(
        raw_text="remind me to check this later",
        awake=True,
        timestamp_utc="2026-01-10T23:55:00Z",
        context=ctx,
        pds={"awake": True},
    )
    out1 = run_engine_via_v1(inp)
    out2 = run_engine_via_v1(inp)
    c1 = to_contract_output(out1, awake_fallback=True)
    c2 = to_contract_output(out2, awake_fallback=True)
    assert c1.get("suggestions") == c2.get("suggestions")


def test_m9w2_context_only_changes_suggestions_not_actions():
    base = EngineInput(
        raw_text="what time is it",
        awake=True,
        timestamp_utc="2026-01-10T23:58:00Z",
        context=None,
        pds={"awake": True},
    )
    with_ctx = EngineInput(
        raw_text="what time is it",
        awake=True,
        timestamp_utc="2026-01-10T23:58:00Z",
        context={"active_app": "Safari", "local_date": "2026-01-10", "local_time": "18:58", "screen_hint": "Reading"},
        pds={"awake": True},
    )

    o1 = run_engine_via_v1(base)
    o2 = run_engine_via_v1(with_ctx)

    assert o1.actions == o2.actions
    assert o1.route_kind == o2.route_kind
