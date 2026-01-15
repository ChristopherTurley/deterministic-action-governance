from v2.coat.coat_v1 import render_hat_event


def test_coat_allow_snapshot():
    e = {
        "type": "HAT_DECISION",
        "hat": "TRADING_HAT_V1",
        "stage": "PROPOSE",
        "decision": "ALLOW",
        "reasons": [],
        "consumed_context_keys": [],
        "proposal_fingerprint": "x",
    }
    out = render_hat_event(e)
    assert out["spoken"] == "Allowed."
    assert "Allowed." in out["display"]
    assert "Hat: TRADING_HAT_V1 | Stage: PROPOSE" in out["display"]


def test_coat_refuse_reason_snapshot():
    e = {
        "type": "HAT_DECISION",
        "hat": "TRADING_HAT_V1",
        "stage": "PROPOSE",
        "decision": "REFUSE",
        "reasons": ["risk_daily_loss_limit_reached_or_exceeded"],
        "consumed_context_keys": [],
        "proposal_fingerprint": "x",
    }
    out = render_hat_event(e)
    assert out["spoken"] == "Refused. Refused: daily loss limit reached."
    assert "Refused: daily loss limit reached." in out["display"]


def test_coat_drift_snapshot():
    e = {
        "type": "HAT_DECISION",
        "hat": "FOCUS_HAT_V1",
        "stage": "COMMIT",
        "decision": "REQUIRE_RECOMMIT",
        "reasons": ["proposal_drift_requires_recommit:task_count"],
        "consumed_context_keys": [],
        "proposal_fingerprint": "x",
    }
    out = render_hat_event(e)
    assert out["spoken"] == "Re-commit required. Re-commit required: proposal changed (task_count)."
    assert "proposal changed (task_count)" in out["display"]


def test_coat_unknown_hat_snapshot():
    e = {
        "type": "HAT_DECISION",
        "hat": "NOPE",
        "stage": "PROPOSE",
        "decision": "REFUSE",
        "reasons": ["unknown_hat:NOPE"],
        "consumed_context_keys": [],
        "proposal_fingerprint": "x",
    }
    out = render_hat_event(e)
    assert out["spoken"] == "Refused. Refused: unknown hat NOPE."
