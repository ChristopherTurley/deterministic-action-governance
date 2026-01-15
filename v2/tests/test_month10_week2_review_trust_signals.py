import json

from v2.contract import to_contract_output
from v2.engine_adapter import EngineInput, run_engine_via_v1


def _contract(raw: str):
    out = run_engine_via_v1(EngineInput(raw_text=raw, awake=True))
    c = to_contract_output(out, awake_fallback=True)
    json.dumps(c)  # JSON-safe
    return c


def test_m10w2_contract_exposes_review_controls_keys_and_version():
    c = _contract("start my day")
    assert c.get("version") == "v2_contract_v1"
    assert (c.get("review_controls_version") or "").strip() != ""
    rc = c.get("review_controls")
    assert isinstance(rc, dict)
    assert isinstance(rc.get("verbs"), list)
    assert isinstance(rc.get("guardrails"), list)
    assert isinstance(rc.get("examples"), list)


def test_m10w2_review_controls_are_deterministic_for_same_input():
    c1 = _contract("start my day")
    c2 = _contract("start my day")
    assert c1.get("review_controls") == c2.get("review_controls")
    assert c1.get("review_controls_version") == c2.get("review_controls_version")


def test_m10w2_review_controls_examples_use_real_suggestion_ids_when_present():
    # Any deterministic input that yields suggestions is acceptable. "start my day" should in v2.
    c = _contract("start my day")
    sug = c.get("suggestions") or []
    rc = c.get("review_controls") or {}
    examples = rc.get("examples") or []

    if not sug:
        # Vacuously OK: examples can still exist, but must be strings
        assert all(isinstance(e, str) for e in examples)
        return

    sid = (sug[0] or {}).get("id")
    assert isinstance(sid, str) and sid.strip()

    # At least one example should reference the real suggestion id
    assert any(sid in str(e) for e in examples)
