import json

from v2.contract import to_contract_output
from v2.engine_adapter import EngineInput, run_engine_via_v1


def _contract(raw: str):
    out = run_engine_via_v1(EngineInput(raw_text=raw, awake=True))
    c = to_contract_output(out, awake_fallback=True)
    json.dumps(c)  # JSON-safe
    return c


def _ledger(c):
    return c.get("review_ledger") or []


def test_m10w3_contract_exposes_review_ledger_keys_and_version():
    c = _contract("start my day")
    assert c.get("version") == "v2_contract_v1"
    assert (c.get("review_ledger_version") or "").strip() != ""
    assert isinstance(c.get("review_ledger"), list)


def test_m10w3_review_ledger_empty_when_no_review_actions():
    c = _contract("start my day")
    assert _ledger(c) == []


def test_m10w3_reject_adds_ledger_entry_metadata_only():
    c = _contract("reject sid123")
    led = _ledger(c)
    assert len(led) == 1
    e = led[0]
    assert e.get("kind") == "SUGGESTION_REJECT"
    assert e.get("suggestion_id") == "sid123"
    assert "note" not in e
    # reject must not create proposals
    assert c.get("proposed_actions") == []


def test_m10w3_defer_adds_ledger_entry_metadata_only():
    c = _contract("defer sid123")
    led = _ledger(c)
    assert len(led) == 1
    e = led[0]
    assert e.get("kind") == "SUGGESTION_DEFER"
    assert e.get("suggestion_id") == "sid123"
    assert "note" not in e
    assert c.get("proposed_actions") == []


def test_m10w3_revise_adds_ledger_entry_with_note_only():
    c = _contract("revise sid123 tighten wording")
    led = _ledger(c)
    assert len(led) == 1
    e = led[0]
    assert e.get("kind") == "SUGGESTION_REVISE"
    assert e.get("suggestion_id") == "sid123"
    assert e.get("note") == "tighten wording"
    # revise must not create proposals
    assert c.get("proposed_actions") == []


def test_m10w3_accept_adds_ledger_entry_and_may_create_proposal_only():
    c = _contract("accept sid123")
    led = _ledger(c)
    assert len(led) == 1
    e = led[0]
    assert e.get("kind") == "SUGGESTION_ACCEPT"
    assert e.get("suggestion_id") == "sid123"
    # proposed_actions are allowed ONLY for accept (proposal-only mapping)
    assert isinstance(c.get("proposed_actions"), list)


def test_m10w3_review_ledger_deterministic_for_same_input():
    c1 = _contract("revise sid123 tighten wording")
    c2 = _contract("revise sid123 tighten wording")
    assert c1.get("review_ledger") == c2.get("review_ledger")
    assert c1.get("review_ledger_version") == c2.get("review_ledger_version")
