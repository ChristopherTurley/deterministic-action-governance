import copy
from v2.engine_adapter import EngineInput, run_engine_via_v1
from v2.contract import to_contract_output

def _ctx():
    return {"active_app":"Safari","local_date":"2026-01-10","local_time":"19:15","screen_hint":"Reading"}

def test_m9w4_contract_always_has_proposed_actions_keys():
    inp = EngineInput(raw_text="what time is it", awake=True, context=_ctx(), pds={"awake": True, "mode":"IDLE"})
    c = to_contract_output(run_engine_via_v1(inp), awake_fallback=True)

    assert c.get("proposed_actions_version") == "proposed_actions_v1"
    pa = c.get("proposed_actions")
    assert isinstance(pa, list)
    # Baseline: no accept -> must be empty (Week4 rule)
    assert pa == []

def test_m9w4_accept_populates_proposed_actions_but_does_not_execute():
    ctx = _ctx()
    pds0 = {"awake": True, "mode":"IDLE"}

    # get stable suggestion id
    c0 = to_contract_output(
        run_engine_via_v1(EngineInput(raw_text="what time is it", awake=True, context=ctx, pds=copy.deepcopy(pds0))),
        awake_fallback=True
    )
    sid = (c0.get("suggestions") or [{}])[0].get("id")
    assert isinstance(sid, str) and sid

    # accept
    c1 = to_contract_output(
        run_engine_via_v1(EngineInput(raw_text=f"accept {sid}", awake=True, context=ctx, pds=copy.deepcopy(pds0))),
        awake_fallback=True
    )

    assert c1.get("proposed_actions_version") == "proposed_actions_v1"
    pa = c1.get("proposed_actions")
    assert isinstance(pa, list)
    assert pa, "expected at least one proposed action after accept"

    # Must NOT add execution actions. "actions" should contain only the explicit accept action.
    acts = c1.get("actions") or []
    assert all(isinstance(a, dict) for a in acts)
    assert any(a.get("kind") == "SUGGESTION_ACCEPT" for a in acts)

    # Proposed actions must be structured + labeled
    p0 = pa[0]
    assert isinstance(p0, dict)
    assert "id" in p0 and isinstance(p0["id"], str) and p0["id"]
    assert "kind" in p0 and isinstance(p0["kind"], str) and p0["kind"]
    assert "payload" in p0 and isinstance(p0["payload"], dict)
    assert "label" in p0 and isinstance(p0["label"], str) and p0["label"]
    assert "reason" in p0 and isinstance(p0["reason"], str) and p0["reason"]

def test_m9w4_proposed_actions_deterministic_for_same_accept():
    ctx = _ctx()
    pds0 = {"awake": True, "mode":"IDLE"}

    c0 = to_contract_output(
        run_engine_via_v1(EngineInput(raw_text="what time is it", awake=True, context=ctx, pds=copy.deepcopy(pds0))),
        awake_fallback=True
    )
    sid = (c0.get("suggestions") or [{}])[0].get("id")
    assert isinstance(sid, str) and sid

    c1 = to_contract_output(
        run_engine_via_v1(EngineInput(raw_text=f"accept {sid}", awake=True, context=ctx, pds=copy.deepcopy(pds0))),
        awake_fallback=True
    )
    c2 = to_contract_output(
        run_engine_via_v1(EngineInput(raw_text=f"accept {sid}", awake=True, context=ctx, pds=copy.deepcopy(pds0))),
        awake_fallback=True
    )

    assert c1.get("proposed_actions") == c2.get("proposed_actions")
