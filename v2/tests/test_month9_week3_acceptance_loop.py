import copy
from v2.engine_adapter import EngineInput, run_engine_via_v1
from v2.contract import to_contract_output
from v2.state_reducer import reduce_pds

def _ctx():
    return {"active_app":"Safari","local_date":"2026-01-10","local_time":"19:05","screen_hint":"Reading"}

def test_m9w3_accept_is_only_trigger_for_suggestion_execution():
    # Baseline produces suggestions but no actions
    inp = EngineInput(raw_text="what time is it", awake=True, timestamp_utc="2026-01-10T00:00:00Z", context=_ctx(), pds={"awake": True, "mode":"IDLE"})
    out = run_engine_via_v1(inp)
    c = to_contract_output(out, awake_fallback=True)
    sug = c.get("suggestions") or []
    assert isinstance(sug, list)

    # If no suggestions exist, test is vacuously true, but we expect at least one CONTEXT_NOTE
    assert sug and isinstance(sug[0], dict)
    sid = sug[0].get("id")
    assert isinstance(sid, str) and sid

    assert c.get("actions") == []

def test_m9w3_accept_emits_explicit_action_and_is_idempotent():
    pds0 = {"awake": True, "mode":"IDLE"}

    # Get a stable suggestion id first
    inp0 = EngineInput(raw_text="what time is it", awake=True, timestamp_utc="2026-01-10T00:00:01Z", context=_ctx(), pds=copy.deepcopy(pds0))
    c0 = to_contract_output(run_engine_via_v1(inp0), awake_fallback=True)
    sid = (c0.get("suggestions") or [{}])[0].get("id")
    assert isinstance(sid, str) and sid

    # Accept should emit exactly one explicit accept action
    inp1 = EngineInput(raw_text=f"accept {sid}", awake=True, timestamp_utc="2026-01-10T00:00:02Z", context=_ctx(), pds=copy.deepcopy(pds0))
    c1 = to_contract_output(run_engine_via_v1(inp1), awake_fallback=True)
    acts = c1.get("actions") or []
    assert isinstance(acts, list)
    assert any(a.get("kind") == "SUGGESTION_ACCEPT" and a.get("payload", {}).get("suggestion_id") == sid for a in acts)

    # Reducer applies acceptance once; second apply is idempotent (no duplicate)
    # (We treat contract actions as "actions" field already normalized in contract.)
    delta = {"accepted_suggestion_id": sid}
    r1 = reduce_pds(copy.deepcopy(pds0), delta)
    r2 = reduce_pds(copy.deepcopy(r1.next_state), delta)
    assert r2.next_state == r1.next_state
