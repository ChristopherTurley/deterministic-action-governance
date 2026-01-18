#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from v2.hats.executive_hat_v1 import ExecutiveHatV1


def main() -> int:
    p = Path("v2/reference/executive_hat_v1/scenarios.json")
    data = json.loads(p.read_text(encoding="utf-8"))

    hat = ExecutiveHatV1()
    out_dir = Path("v2/reference/executive_hat_v1")
    out_dir.mkdir(parents=True, exist_ok=True)

    receipts = []
    for s in data["scenarios"]:
        ctx = s["ctx"]
        proposed = s["proposed"]
        commit = s["commit"] if s["commit"] is not None else dict(proposed)

        prop_out = hat.decide_proposal(ctx, proposed).to_ledger_event()
        com_out = hat.decide_commit(ctx, proposed, commit).to_ledger_event()

        receipts.append(
            {
                "name": s["name"],
                "propose": prop_out,
                "commit": com_out,
            }
        )

    out_path = out_dir / "reference_receipts.json"
    out_path.write_text(json.dumps({"hat_id": "EXECUTIVE_HAT_V1", "receipts": receipts}, indent=2, sort_keys=True), encoding="utf-8")
    print(str(out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
