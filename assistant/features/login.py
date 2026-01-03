from __future__ import annotations
import getpass
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any

PROFILE_DIR = Path("assistant/profiles")
DEFAULT_PROFILE = PROFILE_DIR / "default.json"

@dataclass
class Profile:
    name: str = "Chris"
    timezone: str = "America/New_York"
    preferences: Dict[str, Any] = None

def load_or_create_profile() -> Profile:
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    if not DEFAULT_PROFILE.exists():
        os_user = getpass.getuser()
        DEFAULT_PROFILE.write_text(
            json.dumps(
                {
                    "name": os_user.title() if os_user else "Chris",
                    "timezone": "America/New_York",
                    "preferences": {},
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    data = json.loads(DEFAULT_PROFILE.read_text(encoding="utf-8"))
    return Profile(
        name=data.get("name", "Chris"),
        timezone=data.get("timezone", "America/New_York"),
        preferences=data.get("preferences", {}) or {},
    )
