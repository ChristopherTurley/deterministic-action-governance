from __future__ import annotations

import subprocess
import time
import re
from typing import Tuple, Optional


# --------- subprocess helpers (timeouts prevent freezes) ----------
def _run(cmd: list[str], timeout_s: float = 0.8) -> Tuple[int, str]:
    try:
        p = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout_s)
        out = (p.stdout or "") + (p.stderr or "")
        return p.returncode, out.strip()
    except subprocess.TimeoutExpired:
        return 124, "timeout"
    except Exception as e:
        return 1, str(e)


def _osascript(script: str, timeout_s: float = 0.8) -> Tuple[bool, str]:
    code, out = _run(["osascript", "-e", script], timeout_s=timeout_s)
    return (code == 0), out


# --------- intent parsing ----------
def is_spotify_intent(t: str) -> bool:
    x = (t or "").lower()
    return ("spotify" in x) or ("play music" in x) or ("play some music" in x)

def parse_spotify_command(t: str) -> Tuple[str, str]:
    x = (t or "").strip().lower()
    if "pause" in x:
        return "pause", ""
    if "resume" in x or "play" in x and "spotify" in x and ("pause" not in x):
        # allow: "play lofi on spotify"
        q = re.sub(r".*\bspotify\b", "", x).strip(" .,!-")
        q = re.sub(r"^(play|start)\b", "", q).strip()
        return "play", q
    return "play", re.sub(r"^(play|start)\b", "", x).strip()

def spotify_pause() -> Tuple[bool, str]:
    return _osascript('tell application "Spotify" to pause')

def spotify_play() -> Tuple[bool, str]:
    return _osascript('tell application "Spotify" to play')

def spotify_search_and_play(query: str) -> Tuple[bool, str]:
    # V1: Open Spotify app and start playback. Search/play via API comes later.
    ok1, out1 = _osascript('tell application "Spotify" to activate')
    ok2, out2 = _osascript('tell application "Spotify" to play')
    ok = ok1 and ok2
    return ok, (out2 or out1 or "")

# --------- Spotify play state (cached) ----------
_LAST_STATE: Optional[bool] = None
_LAST_AT: float = 0.0

def spotify_is_playing(cache_ttl_s: float = 0.35) -> bool:
    """
    Fast mic gate:
    - osascript can stall; we timeout.
    - Cache results so we aren't hammering the system.
    """
    global _LAST_STATE, _LAST_AT
    now = time.time()
    if _LAST_STATE is not None and (now - _LAST_AT) <= cache_ttl_s:
        return _LAST_STATE

    script = 'tell application "Spotify" to (player state as string)'
    ok, out = _osascript(script, timeout_s=0.6)
    if not ok:
        # If Spotify is not running, treat as not playing
        # If it timed out, keep last known state (better UX)
        if out == "timeout" and _LAST_STATE is not None:
            return _LAST_STATE
        _LAST_STATE = False
        _LAST_AT = now
        return False

    state = (out or "").strip().lower()
    playing = ("playing" in state)
    _LAST_STATE = playing
    _LAST_AT = now
    return playing


# --------- YouTube helpers ----------
def is_youtube_intent(t: str) -> bool:
    x = (t or "").lower()
    return "youtube" in x or "search youtube" in x or "find on youtube" in x

def parse_youtube_query(t: str) -> str:
    x = (t or "").strip()
    x2 = re.sub(r"(?i)\b(search youtube for|search youtube|find on youtube|youtube)\b", "", x).strip(" ,.!?-")
    return x2 or "lofi work music"

def open_youtube_search(q: str) -> Tuple[bool, str]:
    q = (q or "").strip()
    if not q:
        q = "lofi work music"
    import urllib.parse
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(q)
    code, out = _run(["open", url], timeout_s=0.8)
    return (code == 0), (out or "")
