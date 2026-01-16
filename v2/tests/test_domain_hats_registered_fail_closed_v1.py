from v2.hats.router_v1 import route_proposal, route_commit

HATS = [
    ("OPS_INCIDENT_HAT_V1", "INV_OPS_"),
    ("PLATFORM_ASSISTANTS_LENS_V1", "INV_PLATFORM_"),
    ("EDUCATION_HAT_V1", "INV_EDU_"),
    ("HEALTHCARE_HAT_V1", "INV_HEALTH_"),
    ("COMPETITIVE_SPORTS_HAT_V1", "INV_SPORTS_"),
    ("EXECUTIVE_HAT_V1", "INV_EXEC_"),
    ("HIGH_FOCUS_WORKER_HAT_V1", "INV_FOCUS_"),
    ("DESIGNER_HAT_V1", "INV_DESIGN_"),
    ("ENGINEER_HAT_V1", "INV_ENG_"),
]

def _assert_prefix(hat_name: str, prefix: str, reasons):
    bad = [r for r in reasons if not r.startswith(prefix)]
    assert not bad, f"prefix_mismatch hat={hat_name} expected_prefix={prefix} reasons={reasons}"

def test_domain_hats_registered_and_fail_closed():
    ctx = {"context_as_of_ts": 1000, "context_ttl_seconds": 999999}
    proposal = {"now_ts": 1001}
    commit = {"now_ts": 1002}

    for hat_name, prefix in HATS:
        e1 = route_proposal(hat_name, ctx, proposal)
        assert e1["type"] == "HAT_DECISION"
        assert e1["hat"] == hat_name
        assert e1["stage"] == "PROPOSE"
        assert e1["decision"] in ["REFUSE", "REQUIRE_RECOMMIT"]
        assert isinstance(e1["reasons"], list) and len(e1["reasons"]) >= 1
        _assert_prefix(hat_name, prefix, e1["reasons"])

        e2 = route_commit(hat_name, ctx, proposal, commit)
        assert e2["type"] == "HAT_DECISION"
        assert e2["hat"] == hat_name
        assert e2["stage"] == "COMMIT"
        assert e2["decision"] in ["REFUSE", "REQUIRE_RECOMMIT"]
        assert isinstance(e2["reasons"], list) and len(e2["reasons"]) >= 1
        _assert_prefix(hat_name, prefix, e2["reasons"])
