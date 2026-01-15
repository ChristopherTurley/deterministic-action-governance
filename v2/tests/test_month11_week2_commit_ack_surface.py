# v2/tests/test_month11_week2_commit_ack_surface.py
"""
Month 11 Week 2 — Commit Acknowledgement (contract-only)

Goal:
- Surface an explicit "commit_ack" structure in the v2 contract output
- Derived ONLY from existing EngineOutput.actions (metadata-only)
- No behavior change, no execution, no receipts

Spec (contract-only):
- When an EngineOutput includes action type PROPOSED_ACTION_COMMIT with proposal_id:
  - contract["commit_ack_version"] == "commit_ack_v1"
  - contract["commit_ack"] includes:
      {
        "proposal_id": "<id>",
        "ack": True,
        "source_action_type": "PROPOSED_ACTION_COMMIT"
      }
- If no commit action present:
  - contract["commit_ack"] is [] (or missing is acceptable but preferred present as [])
"""

from v2.engine_adapter import EngineInput, run_engine_via_v1
from v2.contract import to_contract_output


def _ack_list(c):
    a = c.get("commit_ack", [])
    return a if isinstance(a, list) else []


def test_m11w2_commit_ack_present_on_commit_action():
    out = run_engine_via_v1(EngineInput(raw_text="commit pid123", awake=True))
    c = to_contract_output(out, awake_fallback=True)

    assert c.get("version") == "v2_contract_v1"
    assert c.get("commit_ack_version") == "commit_ack_v1"

    acks = _ack_list(c)
    assert any(
        isinstance(a, dict)
        and a.get("proposal_id") == "pid123"
        and a.get("ack") is True
        and a.get("source_action_type") == "PROPOSED_ACTION_COMMIT"
        for a in acks
    )


def test_m11w2_commit_ack_empty_when_no_commit_action():
    out = run_engine_via_v1(EngineInput(raw_text="reject sid123", awake=True))
    c = to_contract_output(out, awake_fallback=True)

    assert c.get("version") == "v2_contract_v1"
    assert c.get("commit_ack_version") == "commit_ack_v1"

    acks = _ack_list(c)
    assert acks == []
