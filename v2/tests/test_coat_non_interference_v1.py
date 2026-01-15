from copy import deepcopy

from v2.coat.coat_v1 import render_hat_event


def test_coat_render_is_non_interfering_transform():
    # render_hat_event() renders a HAT_DECISION payload into a human-facing dict.
    # The coat is allowed to drop non-essential fields, but must preserve decision semantics.
    payload = {
        "type": "HAT_DECISION",
        "hat": "TRADING_HAT_V1",
        "stage": "PROPOSE",
        "decision": "REFUSE",
        "reasons": ["INV_TRADING_CAP_EXCEEDED"],
        "details": {"note": "shape-only"},
    }

    before = deepcopy(payload)
    out = render_hat_event(payload)

    # 1) Input must not be mutated.
    assert payload == before

    # 2) Output must preserve governance-critical fields exactly.
    assert isinstance(out, dict)
    assert out.get("hat") == before["hat"]
    assert out.get("stage") == before["stage"]
    assert out.get("decision") == before["decision"]
    assert out.get("reasons") == before["reasons"]

    # 3) Coat must add human-facing display text, but must not guide action.
    assert "display" in out
    assert isinstance(out["display"], str)
