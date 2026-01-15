from __future__ import annotations

import json

from v2.hats.focus_hat_v1 import FocusHatV1


def _banner(title: str) -> None:
    print("")
    print("================================================================")
    print(title)
    print("================================================================")


def main() -> None:
    hat = FocusHatV1()

    ctx = {
        "focus_mode": "DEEP_WORK",
        "context_as_of_ts": 1000,
        "context_ttl_seconds": 600,
        "task_count_cap": 5,
        "tasks_remaining": 3,
        "minutes_cap": 60,
        "minutes_remaining": 45,
    }

    proposal_ok = {
        "task_count": 2,
        "planned_minutes": 30,
        "now_ts": 1100,
    }

    commit_ok = dict(proposal_ok)

    _banner("SCENARIO A — ALLOW (PROPOSE + COMMIT)")
    out_p = hat.decide_proposal(ctx, proposal_ok)
    print("PROPOSE:", out_p.decision.value)
    if out_p.reasons:
        print("REASONS:", out_p.reasons)
    out_c = hat.decide_commit(ctx, proposal_ok, commit_ok)
    print("COMMIT:", out_c.decision.value)
    if out_c.reasons:
        print("REASONS:", out_c.reasons)

    _banner("SCENARIO B — REFUSE (CAP EXCEEDED)")
    proposal_bad = dict(proposal_ok)
    proposal_bad["task_count"] = 10
    out_b = hat.decide_proposal(ctx, proposal_bad)
    print("PROPOSE:", out_b.decision.value)
    print("REASONS:", out_b.reasons)

    _banner("SCENARIO C — REQUIRE RE-COMMIT (DRIFT)")
    commit_drift = dict(proposal_ok)
    commit_drift["task_count"] = 3
    out_d = hat.decide_commit(ctx, proposal_ok, commit_drift)
    print("COMMIT:", out_d.decision.value)
    print("REASONS:", out_d.reasons)

    _banner("LEDGER EVENTS (SAMPLE)")
    events = [out_p.to_ledger_event(), out_c.to_ledger_event(), out_b.to_ledger_event(), out_d.to_ledger_event()]
    print(json.dumps(events, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
