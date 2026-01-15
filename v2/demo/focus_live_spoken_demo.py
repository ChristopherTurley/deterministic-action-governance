from __future__ import annotations

import subprocess

from v2.coat.coat_v1 import render_hat_event
from v2.hats.router_v1 import route_proposal, route_commit


def say(text: str) -> None:
    try:
        subprocess.run(["say", text], check=False)
    except Exception:
        pass


def banner(t: str) -> None:
    print("")
    print("================================================================")
    print(t)
    print("================================================================")


def main() -> None:
    ctx = {
        "focus_mode": "DEEP_WORK",
        "context_as_of_ts": 1000,
        "context_ttl_seconds": 600,
        "task_count_cap": 5,
        "tasks_remaining": 3,
        "minutes_cap": 60,
        "minutes_remaining": 45,
    }

    banner("FOCUS (SPOKEN) — ALLOW / ALLOW")
    prop = {"task_count": 2, "planned_minutes": 30, "now_ts": 1100}
    com = dict(prop)
    e1 = route_proposal("FOCUS_HAT_V1", ctx, prop)
    o1 = render_hat_event(e1)
    print(o1["display"])
    say(o1["spoken"])

    e2 = route_commit("FOCUS_HAT_V1", ctx, prop, com)
    o2 = render_hat_event(e2)
    print("")
    print(o2["display"])
    say(o2["spoken"])

    banner("FOCUS (SPOKEN) — DRIFT / REQUIRE RE-COMMIT")
    prop2 = {"task_count": 2, "planned_minutes": 30, "now_ts": 1200}
    com2 = {"task_count": 3, "planned_minutes": 30, "now_ts": 1201}
    e3 = route_commit("FOCUS_HAT_V1", ctx, prop2, com2)
    o3 = render_hat_event(e3)
    print(o3["display"])
    say(o3["spoken"])


if __name__ == "__main__":
    main()
