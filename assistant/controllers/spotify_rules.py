from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Optional

@dataclass
class SpotifyAction:
    handled: bool
    cmd: str | None = None          # play | pause | resume | liked | next | prev
    query: str | None = None        # for cmd=play

# Common ASR mishears for "liked"
LIKED_PHRASES = (
    "liked songs",
    "my liked songs",
    "your liked songs",
    "saved songs",
    "my library",
    "liked music",
    "my liked music",
    # mishears:
    "light songs",
    "my light songs",
    "light music",
    "my light music",
    "like songs",
    "my like songs",
)

GLOBAL_CONTROLS = {
    "pause": "pause",
    "resume": "resume",
    "play": "resume",
    "next": "next",
    "skip": "next",
    "previous": "prev",
    "prev": "prev",
    "back": "prev",
}

def _norm(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s

def classify_spotify(text: str) -> Optional[SpotifyAction]:
    """
    Returns SpotifyAction if the utterance is clearly a Spotify/media command.
    Input should be cleaned (wake stripped).
    """
    c = _norm(text)
    c_cmd = c.strip().strip(" .!?,")

    # global controls
    if c_cmd in GLOBAL_CONTROLS:
        return SpotifyAction(True, cmd=GLOBAL_CONTROLS[c_cmd])

    # liked songs/library
    if any(p in c for p in LIKED_PHRASES):
        return SpotifyAction(True, cmd="liked")

    # explicit spotify play: "play X on spotify" or "play X"
    # If user says "play my light music" this is handled above as liked.
    m = re.match(r"^play\s+(.+?)(\s+on\s+spotify)?$", c_cmd)
    if m:
        q = (m.group(1) or "").strip()
        if q:
            return SpotifyAction(True, cmd="play", query=q)

    return None
