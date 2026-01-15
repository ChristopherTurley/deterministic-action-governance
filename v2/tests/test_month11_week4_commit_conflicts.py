# v2/tests/test_month11_week4_commit_conflicts.py
"""
Month 11 Week 4 — Commit Conflicts (Contract-only)

Goal:
- Surface deterministic commit conflict diagnostics derived strictly from commit_ledger.
- No behavior changes. No execution. No receipts invented.

Signals:
- DUPLICATE_ENTRY: same proposal_id committed more than once (duplicate COMMIT_REQUEST entries).
- CONFLICTING_STATES: proposal_id has both COMMIT_REQUEST and COMMIT_ACK (or other mixed kinds).
"""

from dataclasses import replace

from v2.engine_adapter import EngineInput, run_engine_via_v1
from v2.contract import to_contract_output
from v2 import contract as contract_mod


def _contract(raw: str):
    out = run_engine_via_v1(EngineInput(raw_text=raw, awake=True))
    return to_contract_output(out, awake_fallback=True)


def _contract_from_out(out):
    return to_contract_output(out, awake_fallback=True)


def _has_conflict(c, t: str, pid: str):
    for x in (c.get("commit_conflicts") or []):
        if isinstance(x, dict) and x.get("type") == t and x.get("proposal_id") == pid:
            return True
    return False


def test_m11w4_commit_conflicts_present_and_versioned():
    c = _contract("commit pid123")
    assert c.get("version") == "v2_contract_v1"
    assert c.get("commit_conflicts_version") == "commit_conflicts_v1"
    cc = c.get("commit_conflicts")
    assert isinstance(cc, list)


def test_m11w4_duplicate_commit_request_detected():
    out = run_engine_via_v1(EngineInput(raw_text="commit pid123", awake=True))
    # Duplicate the action deterministically (EngineOutput is frozen)
    out2 = replace(out, actions=(out.actions or []) + (out.actions or []))
    c = _contract_from_out(out2)
    # Recompute conflicts from the final contract shape (contract-only diagnostic)
    c['commit_conflicts'] = contract_mod._m11w4_commit_conflicts_from_contract(c)

    # Recompute conflicts from the final contract shape (contract-only diagnostic)
    assert _has_conflict(c, "DUPLICATE_ENTRY", "pid123")


def test_m11w4_conflicting_kinds_detected_for_same_proposal_id():
    out_commit = run_engine_via_v1(EngineInput(raw_text="commit pid123", awake=True))
    c_commit = _contract_from_out(out_commit)

    # Build a synthetic output dict-shaped contract and inject a COMMIT_ACK ledger entry
    # by duplicating + altering commit_ledger post-contract (contract-only diagnostic test).
    led = list(c_commit.get("commit_ledger") or [])
    led.append({"kind": "COMMIT_ACK", "proposal_id": "pid123"})
    c_commit["commit_ledger"] = led

    # Re-run just the conflict derivation by round-tripping through to_contract_output() shape:
    # We do this by creating a minimal engine-like output and letting contract rebuild, then overwrite ledger.
    base = run_engine_via_v1(EngineInput(raw_text="commit pid123", awake=True))
    c2 = to_contract_output(base, awake_fallback=True)
    c2["commit_ledger"] = led


    # Recompute conflicts after injecting ledger (contract-only diagnostic)
    c2["commit_conflicts"] = contract_mod._m11w4_commit_conflicts_from_contract(c2)

    # Conflict surface must flag mixed kinds for same proposal id.
    assert _has_conflict(c2, "CONFLICTING_STATES", "pid123")
