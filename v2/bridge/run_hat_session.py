from __future__ import annotations

import argparse
import json
import os
import sys
import time
import subprocess
from typing import Any, Dict, List

from v2.coat.coat_v1 import render_hat_event
from v2.hats.router_v1 import route_proposal, route_commit
from v2.hats.registry import list_hats


def _say(text: str, enabled: bool) -> None:
    if not enabled:
        return
    try:
        subprocess.run(["say", text], check=False)
    except Exception:
        pass


def _load_json_arg(s: str) -> Dict[str, Any]:
    try:
        obj = json.loads(s)
        if not isinstance(obj, dict):
            raise ValueError("JSON must be an object")
        return obj
    except Exception as e:
        raise ValueError("Invalid JSON object: " + str(e))


def _now_ts() -> int:
    return int(time.time())


def _ensure_ts(obj: Dict[str, Any], key: str) -> None:
    if key not in obj or obj.get(key) is None:
        obj[key] = _now_ts()


def main() -> None:
    p = argparse.ArgumentParser(description="VERA v2 Hat Session Bridge (opt-in; does not touch v1).")
    p.add_argument("--hat", required=True, help="Hat name (e.g., TRADING_HAT_V1, FOCUS_HAT_V1)")
    p.add_argument("--context", required=True, help="JSON object string for context")
    p.add_argument("--proposal", required=True, help="JSON object string for proposal")
    p.add_argument("--commit", required=True, help="JSON object string for commit")
    p.add_argument("--speak", action="store_true", help="Speak coat output using macOS say")
    p.add_argument("--ledger-out", default="v2/demo/hat_session_ledger.json", help="Path to write ledger JSON")
    args = p.parse_args()

    hat = (args.hat or "").strip().upper()
    if hat not in list_hats():
        print("REFUSE: unknown hat:", hat)
        print("Known hats:", ", ".join(list_hats()))
        sys.exit(2)

    ctx = _load_json_arg(args.context)
    prop = _load_json_arg(args.proposal)
    com = _load_json_arg(args.commit)

    # Ensure timestamps (without mutating semantics)
    _ensure_ts(ctx, "context_as_of_ts")
    # Proposal/commit use now_ts only if hat expects it; safe to provide.
    _ensure_ts(prop, "now_ts")
    _ensure_ts(com, "now_ts")

    ledger: List[Dict[str, Any]] = []

    # PROPOSE
    e_p = route_proposal(hat, ctx, prop)
    coated_p = render_hat_event(e_p)
    ledger.append({"type": "HAT_DECISION", "payload": e_p, "ts": _now_ts()})

    print("")
    print("=== PROPOSE (COATED) ===")
    print(coated_p["display"])
    _say(coated_p["spoken"], args.speak)

    if e_p.get("decision") == "REFUSE":
        _write_ledger(args.ledger_out, ctx, prop, None, ledger)
        sys.exit(1)

    # COMMIT
    e_c = route_commit(hat, ctx, prop, com)
    coated_c = render_hat_event(e_c)
    ledger.append({"type": "HAT_DECISION", "payload": e_c, "ts": _now_ts()})

    print("")
    print("=== COMMIT (COATED) ===")
    print(coated_c["display"])
    _say(coated_c["spoken"], args.speak)

    _write_ledger(args.ledger_out, ctx, prop, com, ledger)

    # Exit codes are deterministic and useful in automation
    if e_c.get("decision") == "ALLOW":
        sys.exit(0)
    if e_c.get("decision") == "REQUIRE_RECOMMIT":
        sys.exit(3)
    sys.exit(1)


def _write_ledger(path: str, ctx: Dict[str, Any], prop: Dict[str, Any], com: Dict[str, Any] | None, events: List[Dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    out = {
        "context": ctx,
        "proposal": prop,
        "commit": com,
        "events": events,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=True)


if __name__ == "__main__":
    main()
