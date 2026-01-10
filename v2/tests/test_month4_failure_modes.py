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
