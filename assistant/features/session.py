from __future__ import annotations

import getpass
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Optional

PROFILE_DIR = Path("assistant/profiles")
PROFILE_PATH = PROFILE_DIR / "default.json"
SESSION_PATH = PROFILE_DIR / "last_session.json"

@dataclass
class Profile:
    name: str
    timezone: str = "America/New_York"
    preferences: Dict[str, Any] = None

def load_profile() -> Profile:
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)

    if not PROFILE_PATH.exists():
        os_user = getpass.getuser() or "Chris"
        PROFILE_PATH.write_text(json.dumps({
            "name": os_user.title(),
            "timezone": "America/New_York",
            "preferences": {
                "brief_blocks": ["morning", "midday", "afternoon"],
                "tone": "ruthless",
            }
        }, indent=2), encoding="utf-8")

    data = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    return Profile(
        name=data.get("name") or "Chris",
        timezone=data.get("timezone") or "America/New_York",
        preferences=data.get("preferences") or {},
    )

def load_last_session() -> Dict[str, Any]:
    if not SESSION_PATH.exists():
        return {}
    try:
        return json.loads(SESSION_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}

def save_session(event: str, extra: Optional[Dict[str, Any]] = None) -> None:
    payload = {
        "event": event,
        "ts": time.time(),
        "extra": extra or {},
    }
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    SESSION_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
