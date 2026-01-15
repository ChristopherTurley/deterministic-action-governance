from v2.hats.router_v1 import route_proposal, route_commit
from v2.coat.coat_v1 import render_hat_event


def _assert_fail_closed(out: dict, hat: str, stage: str) -> None:
    assert isinstance(out, dict)
    assert out.get("hat") == hat
    assert out.get("stage") == stage
    assert out.get("decision") == "REFUSE"

    reasons = out.get("reasons")
    assert isinstance(reasons, list)
    assert len(reasons) >= 1
    assert all(isinstance(r, str) and r for r in reasons)

    rendered = render_hat_event(out)
    assert isinstance(rendered, dict)
    assert rendered.get("decision") == "REFUSE"
    assert rendered.get("hat") == hat
    assert rendered.get("stage") == stage
    assert isinstance(rendered.get("display"), str)
    assert rendered["display"].strip() != ""
    # Ensure the display includes at least one reason code for audit legibility.
    assert any(r in rendered["display"] for r in reasons)


def test_unknown_hat_proposal_is_fail_closed_and_renderable():
    hat = "MADE_UP_HAT"
    out = route_proposal(hat, {}, {})
    _assert_fail_closed(out, hat, "PROPOSE")


def test_unknown_hat_commit_is_fail_closed_and_renderable():
    hat = "MADE_UP_HAT"
    out = route_commit(hat, {}, {}, {})
    _assert_fail_closed(out, hat, "COMMIT")
