#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from v2.hats.trading_hat_v1 import evaluate


def main() -> int:
    p = Path("v2/reference/trading_hat_v1/scenarios.json")
    data = json.loads(p.read_text(encoding="utf-8"))
    out_dir = Path("v2/reference/trading_hat_v1")
    out_dir.mkdir(parents=True, exist_ok=True)

    receipts = []
    for s in data["scenarios"]:
        r = evaluate(s["input"], int(s["logical_time_index"]))
        receipts.append({"name": s["name"], "receipt": r})

    out_path = out_dir / "reference_receipts.json"
    out_path.write_text(json.dumps({"hat_id": "TRADING_HAT_V1", "receipts": receipts}, indent=2, sort_keys=True), encoding="utf-8")
    print(str(out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
