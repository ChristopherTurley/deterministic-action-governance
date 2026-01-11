import json
from dataclasses import replace

from v2.contract import to_contract_output
from v2.engine_adapter import EngineInput, run_engine_via_v1


def _c(raw: str):
    out = run_engine_via_v1(EngineInput(raw_text=raw, awake=True))
    c = to_contract_output(out, awake_fallback=True)
    json.dumps(c)
    return c


def test_m10w4_contract_exposes_review_conflicts_keys_and_version():
    c = _c("start my day")
    assert c.get("version") == "v2_contract_v1"
    assert (c.get("review_conflicts_version") or "").strip() != ""
    assert isinstance(c.get("review_conflicts"), list)


def test_m10w4_no_conflicts_for_single_review_action():
    c = _c("reject sid123")
    assert c.get("review_conflicts") == []


def test_m10w4_duplicate_entry_detected_when_actions_repeat():
    out = run_engine_via_v1(EngineInput(raw_text="reject sid123", awake=True))
    out2 = replace(out, actions=(out.actions or []) + (out.actions or []))
    c = to_contract_output(out2, awake_fallback=True)
    conf = c.get("review_conflicts") or []
    assert any(
        x.get("type") == "DUPLICATE_ENTRY" and x.get("suggestion_id") == "sid123"
        for x in conf
    )


def test_m10w4_conflicting_verbs_detected_for_same_suggestion_id():
    out_reject = run_engine_via_v1(EngineInput(raw_text="reject sid123", awake=True))
    out_defer = run_engine_via_v1(EngineInput(raw_text="defer sid123", awake=True))

    out_combo = replace(
        out_reject,
        actions=(out_reject.actions or []) + (out_defer.actions or []),
    )
    c = to_contract_output(out_combo, awake_fallback=True)

    conf = c.get("review_conflicts") or []
    hit = [
        x
        for x in conf
        if x.get("type") == "CONFLICTING_VERBS" and x.get("suggestion_id") == "sid123"
    ]
    assert hit, "Expected CONFLICTING_VERBS for sid123"
    verbs = hit[0].get("verbs") or []
    assert sorted(verbs) == sorted(["SUGGESTION_DEFER", "SUGGESTION_REJECT"])
