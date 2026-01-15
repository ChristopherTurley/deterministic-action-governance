import json

from v2.contract import to_contract_output
from v2.engine_adapter import EngineInput, run_engine_via_v1


def _contract(raw: str):
    out = run_engine_via_v1(EngineInput(raw_text=raw, awake=True))
    c = to_contract_output(out, awake_fallback=True)
    json.dumps(c)  # JSON-safe contract
    return c


def _has_action(c, kind: str, proposal_id: str) -> bool:
    acts = c.get("actions") or []
    for a in acts:
        if (a.get("kind") or "") == kind and (a.get("payload") or {}).get("proposal_id") == proposal_id:
            return True
    return False


def test_m11w1_contract_surfaces_commit_controls_and_versions():
    c = _contract("start my day")
    assert c.get("version") == "v2_contract_v1"

    assert (c.get("commit_controls_version") or "").strip() != ""
    assert isinstance(c.get("commit_controls"), dict)

    assert (c.get("commit_requests_version") or "").strip() != ""
    assert isinstance(c.get("commit_requests"), list)

    assert (c.get("commit_conflicts_version") or "").strip() != ""
    assert isinstance(c.get("commit_conflicts"), list)


def test_m11w1_commit_emits_metadata_action_only_no_execution():
    c = _contract("commit pid123")
    assert c.get("version") == "v2_contract_v1"
    assert _has_action(c, "PROPOSED_ACTION_COMMIT", "pid123")

    # Still proposal-only system: commit does not execute or create receipts
    assert (c.get("receipts") or []) == []


def test_m11w1_commit_unknown_proposal_id_is_flagged_when_no_proposals_exist():
    c = _contract("commit pid123")
    assert (c.get("proposed_actions") or []) == []  # no accept -> no proposals
    conf = c.get("commit_conflicts") or []
    assert any(x.get("type") == "UNKNOWN_PROPOSAL_ID" and x.get("proposal_id") == "pid123" for x in conf)


def test_m11w1_commit_is_deterministic_for_same_input():
    c1 = _contract("commit pid123")
    c2 = _contract("commit pid123")
    assert c1.get("actions") == c2.get("actions")
    assert c1.get("commit_requests") == c2.get("commit_requests")
    assert c1.get("commit_conflicts") == c2.get("commit_conflicts")
