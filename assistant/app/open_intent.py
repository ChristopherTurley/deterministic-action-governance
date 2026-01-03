from __future__ import annotations

import re
from typing import Optional


def parse_open_choice(text: str) -> Optional[int]:
    """
    Returns:
      - 0 for 'best' / 'open it'
      - 1..9 for 'open 1', 'open article 2', etc.
      - None if not an open intent
    """
    t = (text or "").strip().lower()

    # best / generic
    if any(p in t for p in ["open it", "open that", "open the link", "open link", "show me", "pull it up", "bring it up", "take me there"]):
        return 0

    # open article 1 / open result 2 / open 3
    m = re.search(r"\bopen\s+(?:article|result|option)?\s*([1-9])\b", t)
    if m:
        return int(m.group(1))

    return None
