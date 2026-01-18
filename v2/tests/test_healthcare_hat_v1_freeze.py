from __future__ import annotations

import json
from pathlib import Path

from v2.hats.healthcare_hat_v1 import HealthcareHatV1
from v2.hats.hat_interface import HatDecision


def test_healthcare_hat_reference_scenarios_are_stable():
    data = json.loads(Path("v2/reference/healthcare_hat_v1/scenarios.json").read_text(encoding="utf-8"))
    prefix = data["expected_prefix"]
    hat = HealthcareHatV1()

    for s in data["scenarios"]:
        ctx = s["ctx"]
        proposed = s["proposed"]
        commit = s["commit"] if s["commit"] is not None else dict(proposed)

        out_p = hat.decide_proposal(ctx, proposed)
        assert out_p.hat == "HEALTHCARE_HAT_V1"
        assert out_p.stage == "PROPOSE"
        assert out_p.decision in (HatDecision.ALLOW, HatDecision.REFUSE, HatDecision.REQUIRE_RECOMMIT)
        if out_p.decision != HatDecision.ALLOW:
            assert all(r.startswith(prefix) for r in out_p.reasons)

        out_c = hat.decide_commit(ctx, proposed, commit)
        assert out_c.hat == "HEALTHCARE_HAT_V1"
        assert out_c.stage == "COMMIT"
        assert out_c.decision in (HatDecision.ALLOW, HatDecision.REFUSE, HatDecision.REQUIRE_RECOMMIT)
        if out_c.decision != HatDecision.ALLOW:
            assert all(r.startswith(prefix) for r in out_c.reasons)

        exp_p = s.get("expect_propose")
        if exp_p:
            assert out_p.decision.value == exp_p["decision"]
            if "reason_contains" in exp_p:
                assert any(exp_p["reason_contains"] in r for r in out_p.reasons)

        exp_c = s.get("expect_commit")
        if exp_c:
            assert out_c.decision.value == exp_c["decision"]
            if "reason_contains" in exp_c:
                assert any(exp_c["reason_contains"] in r for r in out_c.reasons)
