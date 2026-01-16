from __future__ import annotations

from typing import Dict, List

from v2.hats.trading_hat_v1 import TradingHatV1
from v2.hats.focus_hat_v1 import FocusHatV1


def list_hats() -> List[str]:
    # Canonical: derive from HAT_REGISTRY (single source of truth).
    # We return only canonical UPPERCASE hat keys (exclude lowercase aliases).
    if "HAT_REGISTRY" not in globals():
        return []
    return sorted([k for k in HAT_REGISTRY.keys() if k == k.upper()])


def get_hat(name: str):
    # Canonical: resolve via HAT_REGISTRY deterministically.
    if "HAT_REGISTRY" not in globals():
        return None

    raw = (name or "").strip()
    candidates = []
    if raw:
        candidates = [raw, raw.upper(), raw.lower()]

    for key in candidates:
        cls = HAT_REGISTRY.get(key)
        if cls is not None:
            return cls()

    return None


# === CANONICAL HAT REGISTRY TABLE (LOCKED) ===
# This table is the single source of truth for hat registration.
# It must exist before any appended registrations below.
HAT_REGISTRY = {}

# === CANONICAL HAT REGISTRATION (LOCKED) ===
# Deterministic registration only. No execution, no branching behavior.

from v2.hats.trading_hat_v1 import TradingHatV1
from v2.hats.ops_incident_hat_v1 import OpsIncidentHatV1
from v2.hats.platform_assistants_lens_v1 import PlatformAssistantsLensV1
from v2.hats.education_hat_v1 import EducationHatV1
from v2.hats.healthcare_hat_v1 import HealthcareHatV1
from v2.hats.competitive_sports_hat_v1 import CompetitiveSportsHatV1
from v2.hats.executive_hat_v1 import ExecutiveHatV1
from v2.hats.high_focus_worker_hat_v1 import HighFocusWorkerHatV1
from v2.hats.designer_hat_v1 import DesignerHatV1
from v2.hats.engineer_hat_v1 import EngineerHatV1

# HAT_REGISTRY must already exist by invariant.
HAT_REGISTRY["trading_hat_v1"] = TradingHatV1

HAT_REGISTRY["TRADING_HAT_V1"] = TradingHatV1

HAT_REGISTRY["FOCUS_HAT_V1"] = FocusHatV1

HAT_REGISTRY["OPS_INCIDENT_HAT_V1"] = OpsIncidentHatV1

HAT_REGISTRY["PLATFORM_ASSISTANTS_LENS_V1"] = PlatformAssistantsLensV1

HAT_REGISTRY["EDUCATION_HAT_V1"] = EducationHatV1

HAT_REGISTRY["HEALTHCARE_HAT_V1"] = HealthcareHatV1

HAT_REGISTRY["COMPETITIVE_SPORTS_HAT_V1"] = CompetitiveSportsHatV1

HAT_REGISTRY["EXECUTIVE_HAT_V1"] = ExecutiveHatV1

HAT_REGISTRY["HIGH_FOCUS_WORKER_HAT_V1"] = HighFocusWorkerHatV1

HAT_REGISTRY["DESIGNER_HAT_V1"] = DesignerHatV1

HAT_REGISTRY["ENGINEER_HAT_V1"] = EngineerHatV1


# === DOMAIN HATS (CANONICAL REGISTRATION) ===
# This section is load-bearing:
# - explicit imports (fail fast on missing files)
# - explicit keys (router must resolve these exact names)

from v2.hats.ops_incident_hat_v1 import OpsIncidentHatV1
from v2.hats.platform_assistants_lens_v1 import PlatformAssistantsLensV1
from v2.hats.education_hat_v1 import EducationHatV1
from v2.hats.healthcare_hat_v1 import HealthcareHatV1
from v2.hats.competitive_sports_hat_v1 import CompetitiveSportsHatV1
from v2.hats.executive_hat_v1 import ExecutiveHatV1
from v2.hats.high_focus_worker_hat_v1 import HighFocusWorkerHatV1
from v2.hats.designer_hat_v1 import DesignerHatV1
from v2.hats.engineer_hat_v1 import EngineerHatV1

HAT_REGISTRY["OPS_INCIDENT_HAT_V1"] = OpsIncidentHatV1
HAT_REGISTRY["PLATFORM_ASSISTANTS_LENS_V1"] = PlatformAssistantsLensV1
HAT_REGISTRY["EDUCATION_HAT_V1"] = EducationHatV1
HAT_REGISTRY["HEALTHCARE_HAT_V1"] = HealthcareHatV1
HAT_REGISTRY["COMPETITIVE_SPORTS_HAT_V1"] = CompetitiveSportsHatV1
HAT_REGISTRY["EXECUTIVE_HAT_V1"] = ExecutiveHatV1
HAT_REGISTRY["HIGH_FOCUS_WORKER_HAT_V1"] = HighFocusWorkerHatV1
HAT_REGISTRY["DESIGNER_HAT_V1"] = DesignerHatV1
HAT_REGISTRY["ENGINEER_HAT_V1"] = EngineerHatV1

# === DOMAIN HATS (LOWERCASE ALIASES) ===
# Registry lookup may normalize hat names; these aliases preserve deterministic routing.
HAT_REGISTRY["ops_incident_hat_v1"] = OpsIncidentHatV1
HAT_REGISTRY["platform_assistants_lens_v1"] = PlatformAssistantsLensV1
HAT_REGISTRY["education_hat_v1"] = EducationHatV1
HAT_REGISTRY["healthcare_hat_v1"] = HealthcareHatV1
HAT_REGISTRY["competitive_sports_hat_v1"] = CompetitiveSportsHatV1
HAT_REGISTRY["executive_hat_v1"] = ExecutiveHatV1
HAT_REGISTRY["high_focus_worker_hat_v1"] = HighFocusWorkerHatV1
HAT_REGISTRY["designer_hat_v1"] = DesignerHatV1
HAT_REGISTRY["engineer_hat_v1"] = EngineerHatV1

