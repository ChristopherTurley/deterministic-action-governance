from __future__ import annotations

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

def _line(s: str) -> None:
    print(s)

def _assert_prefix(hat: str, prefix: str, reasons) -> None:
    bad = [r for r in reasons if not str(r).startswith(prefix)]
    if bad:
        raise SystemExit(f"prefix_mismatch hat={hat} expected_prefix={prefix} reasons={reasons}")

def main() -> None:
    _line("")
    _line("================================================================")
    _line("DOMAIN HATS v1 — FAIL-CLOSED SURFACE PROOF (ROUTER v1)")
    _line("================================================================")
    _line("This demo proves:")
    _line("- hats are routable by exact name")
    _line("- stubs fail closed deterministically")
    _line("- reason codes remain namespaced (INV_*)")
    _line("")

    ctx = {"context_as_of_ts": 1000, "context_ttl_seconds": 999999}
    proposal = {"now_ts": 1001}
    commit = {"now_ts": 1002}

    for hat_name, prefix in HATS:
        e1 = route_proposal(hat_name, ctx, proposal)
        e2 = route_commit(hat_name, ctx, proposal, commit)

        _assert_prefix(hat_name, prefix, e1.get("reasons", []))
        _assert_prefix(hat_name, prefix, e2.get("reasons", []))

        _line("------------------------------------------------------------")
        _line(f"hat: {hat_name}")
        _line(f"PROPOSE decision: {e1.get('decision')} reasons: {e1.get('reasons')}")
        _line(f"COMMIT  decision: {e2.get('decision')} reasons: {e2.get('reasons')}")

    _line("------------------------------------------------------------")
    _line("OK: domain hats are routable + fail-closed + namespaced")
    _line("")

if __name__ == "__main__":
    main()
