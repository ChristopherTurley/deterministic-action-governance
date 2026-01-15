from v2.hats.focus_hat_v1 import FocusHatV1
from v2.hats.hat_interface import HatDecision


def _ctx(now: int = 1000):
    return {
        "focus_mode": "DEEP_WORK",
        "context_as_of_ts": now,
        "context_ttl_seconds": 600,
        "task_count_cap": 5,
        "tasks_remaining": 3,
        "minutes_cap": 60,
        "minutes_remaining": 45,
    }


def test_refuse_missing_context_key():
    hat = FocusHatV1()
    ctx = _ctx()
    del ctx["task_count_cap"]
    proposal = {"task_count": 1, "now_ts": 1000}
    out = hat.decide_proposal(ctx, proposal)
    assert out.decision == HatDecision.REFUSE
    assert "context_missing_required_key:task_count_cap" in out.reasons


def test_refuse_stale_context():
    hat = FocusHatV1()
    ctx = _ctx(now=0)
    ctx["context_ttl_seconds"] = 10
    proposal = {"task_count": 1, "now_ts": 1000}
    out = hat.decide_proposal(ctx, proposal)
    assert out.decision == HatDecision.REFUSE
    assert "context_stale_ttl_exceeded" in out.reasons


def test_refuse_missing_task_count():
    hat = FocusHatV1()
    ctx = _ctx()
    proposal = {"now_ts": 1000}
    out = hat.decide_proposal(ctx, proposal)
    assert out.decision == HatDecision.REFUSE
    assert "proposal_missing_required_key:task_count" in out.reasons


def test_refuse_task_count_exceeds_cap():
    hat = FocusHatV1()
    ctx = _ctx()
    proposal = {"task_count": 10, "now_ts": 1000}
    out = hat.decide_proposal(ctx, proposal)
    assert out.decision == HatDecision.REFUSE
    assert "focus_task_count_exceeds_cap" in out.reasons


def test_allow_happy_path_with_minutes():
    hat = FocusHatV1()
    ctx = _ctx()
    proposal = {"task_count": 2, "planned_minutes": 30, "now_ts": 1000}
    out = hat.decide_proposal(ctx, proposal)
    assert out.decision == HatDecision.ALLOW


def test_refuse_planned_minutes_exceeds_remaining():
    hat = FocusHatV1()
    ctx = _ctx()
    proposal = {"task_count": 1, "planned_minutes": 999, "now_ts": 1000}
    out = hat.decide_proposal(ctx, proposal)
    assert out.decision == HatDecision.REFUSE
    assert "focus_planned_minutes_exceeds_cap" in out.reasons or "focus_planned_minutes_exceeds_remaining" in out.reasons


def test_require_recommit_on_task_count_drift():
    hat = FocusHatV1()
    ctx = _ctx()
    proposed = {"task_count": 2, "planned_minutes": 30, "now_ts": 1000}
    commit = {"task_count": 3, "planned_minutes": 30, "now_ts": 1001}
    out = hat.decide_commit(ctx, proposed, commit)
    assert out.decision == HatDecision.REQUIRE_RECOMMIT
    assert out.reasons
    assert "proposal_drift_requires_recommit:task_count" in out.reasons[0]
