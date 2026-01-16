from __future__ import annotations

from typing import Dict, List

from v2.hats.trading_hat_v1 import TradingHatV1
from v2.hats.focus_hat_v1 import FocusHatV1


def list_hats() -> List[str]:
    return sorted(["TRADING_HAT_V1", "FOCUS_HAT_V1"])


def get_hat(name: str):
    n = (name or "").strip().upper()
    if n == "TRADING_HAT_V1":
        return TradingHatV1()
    if n == "FOCUS_HAT_V1":
        return FocusHatV1()
    return None


# === CANONICAL HAT REGISTRY TABLE (LOCKED) ===
# This table is the single source of truth for hat registration.
# It must exist before any appended registrations below.
HAT_REGISTRY = {}

# === CANONICAL HAT REGISTRATION (LOCKED) ===
# Deterministic registration only. No execution, no branching behavior.

from v2.hats.trading_hat_v1 import TradingHatV1

# HAT_REGISTRY must already exist by invariant.
HAT_REGISTRY["trading_hat_v1"] = TradingHatV1

HAT_REGISTRY["TRADING_HAT_V1"] = TradingHatV1

HAT_REGISTRY["FOCUS_HAT_V1"] = FocusHatV1
