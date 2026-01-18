from __future__ import annotations

import re
import json
from pathlib import Path

from v2.hats.reason_allowlists_v1 import ALLOWLISTS_V1

def _token(reason: str) -> str:
    # reason format: PREFIX + token + optional ":" + detail
    # Example: "INV_EXEC_missing_context_keys:role" -> "missing_context_keys"
    # We don't assume the exact prefix; we strip up to the first token boundary by splitting on "_" and taking the tail.
    # Safer: find last prefix segment "INV_*_" then parse remainder.
    # Minimal: remove leading "INV_*_" pattern if present.
    m = re.match(r"^INV_[A-Z]+_(.+)$", reason)
    s = m.group(1) if m else reason
    # token ends at ":" if present
    return s.split(":", 1)[0]

def test_reason_tokens_are_allowlisted_for_frozen_hats():
    # This test is intentionally light-touch:
    # - It inspects reference receipts (deterministic, committed outputs)
    # - It verifies every emitted reason token is allowlisted for that hat
    for hat_id, allowed in ALLOWLISTS_V1.items():
        # Map hat_id -> reference receipts location (only hats present so far)
        if hat_id == "TRADING_HAT_V1":
            p = Path("v2/reference/trading_hat_v1/reference_receipts.json")
        elif hat_id == "EXECUTIVE_HAT_V1":
            p = Path("v2/reference/executive_hat_v1/reference_receipts.json")
        elif hat_id == "OPS_INCIDENT_HAT_V1":
            p = Path("v2/reference/ops_incident_hat_v1/reference_receipts.json")
        else:
            continue

        data = json.loads(p.read_text(encoding="utf-8"))
        receipts = data.get("receipts", [])
        assert receipts, f"no receipts found for {hat_id}"

        for r in receipts:
            for stage in ["propose", "commit"]:
                ev = r.get(stage, {})
                reasons = ev.get("reasons", [])
                for reason in reasons:
                    tok = _token(reason)
                    assert tok in allowed, f"reason_token_not_allowlisted hat={hat_id} token={tok} reason={reason}"
