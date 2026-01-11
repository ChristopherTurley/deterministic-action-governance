import json

from v2.contract import to_contract_output
from v2.engine_adapter import EngineInput, run_engine_via_v1


def _contract_for_raw(raw: str):
    out = run_engine_via_v1(EngineInput(raw_text=raw, awake=True))
    c = to_contract_output(out, awake_fallback=True)
    json.dumps(c)  # JSON-safe invariant
    return c


def _has_action(c, kind: str, suggestion_id: str, note: str | None = None) -> bool:
    acts = c.get("actions") or []
    for a in acts:
        if a.get("kind") != kind:
            continue
        payload = a.get("payload") or {}
        if payload.get("suggestion_id") != suggestion_id:
            continue
        if note is not None and payload.get("note") != note:
            continue
        return True
    return False


def test_reject_emits_metadata_action_only_and_no_proposals():
    c = _contract_for_raw("reject sid123")
    assert c.get("version") == "v2_contract_v1"
    assert _has_action(c, "SUGGESTION_REJECT", "sid123")
    assert c.get("proposed_actions") == []


def test_defer_emits_metadata_action_only_and_no_proposals():
    c = _contract_for_raw("defer sid123")
    assert _has_action(c, "SUGGESTION_DEFER", "sid123")
    assert c.get("proposed_actions") == []


def test_revise_emits_metadata_action_with_note_only_and_no_proposals():
    c = _contract_for_raw("revise sid123 tighten wording")
    assert _has_action(c, "SUGGESTION_REVISE", "sid123", note="tighten wording")
    assert c.get("proposed_actions") == []


def test_review_controls_are_idempotent_for_same_input_contract_surface():
    c1 = _contract_for_raw("defer sid123")
    c2 = _contract_for_raw("defer sid123")
    assert c1 == c2
