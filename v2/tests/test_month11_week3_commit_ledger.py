# v2/tests/test_month11_week3_commit_ledger.py
"""
Month 11 Week 3 — Commit Ledger (contract-only)

Purpose:
- Surface a deterministic commit ledger derived from metadata-only commit requests + commit ack.
- Contract-only: no behavior change, no execution, no receipts changes.
"""

from v2.engine_adapter import EngineInput, run_engine_via_v1
from v2.contract import to_contract_output


def _contract(raw: str):
    out = run_engine_via_v1(EngineInput(raw_text=raw, awake=True))
    return to_contract_output(out, awake_fallback=True)


def test_m11w3_commit_ledger_present_and_versioned():
    c = _contract("commit pid123")
    assert c.get("version") == "v2_contract_v1"
    assert c.get("commit_ledger_version") == "commit_ledger_v1"
    led = c.get("commit_ledger")
    assert isinstance(led, list)
    assert len(led) >= 1


def test_m11w3_commit_ledger_entry_contains_proposal_id_and_kind():
    c = _contract("commit pid123")
    led = c.get("commit_ledger") or []

    has = False
    for e in led:
        if not isinstance(e, dict):
            continue
        if e.get("proposal_id") == "pid123" and e.get("kind") == "COMMIT_REQUEST":
            has = True
            break

    assert has, f"expected COMMIT_REQUEST for pid123 in commit_ledger, got: {led}"


def test_m11w3_commit_ledger_is_metadata_only_no_receipts_added():
    c = _contract("commit pid123")
    assert (c.get("receipts") or []) == []


def test_m11w3_commit_ledger_empty_when_no_commit_activity():
    c = _contract("what time is it")
    assert c.get("version") == "v2_contract_v1"
    led = c.get("commit_ledger") or []
    assert led == []
