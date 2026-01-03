from __future__ import annotations

import subprocess
from typing import Optional, Tuple


def _osascript(script: str) -> Tuple[bool, str]:
    """
    Run AppleScript and return (ok, message).
    Always returns a message so callers can log/speak real errors.
    """
    try:
        out = subprocess.check_output(["osascript", "-e", script], stderr=subprocess.STDOUT, text=True)
        out = (out or "").strip()
        return True, out or "OK"
    except subprocess.CalledProcessError as e:
        msg = (e.output or "").strip()
        return False, msg or f"osascript failed (code {e.returncode})"


def liked_songs() -> Tuple[bool, str]:
    # This reliably starts Liked Songs from the top on many Spotify builds.
    script = '''
    try
      tell application "Spotify" to activate
      delay 0.1
      tell application "Spotify" to play track "spotify:collection"
      return "OK play collection"
    on error errMsg number errNum
      return "ERROR " & errNum & ": " & errMsg
    end try
    '''
    ok, msg = _osascript(script)
    if ok and msg.startswith("ERROR"):
        return False, msg
    return ok, msg


def play(query: Optional[str] = None) -> Tuple[bool, str]:
    # Basic play: if query is empty, just play
    if query:
        # NOTE: search+play requires Spotify API; AppleScript can't search reliably.
        # We'll just start playback and report that search is unsupported via AppleScript.
        ok, msg = _osascript('tell application "Spotify" to play')
        if ok:
            return True, f"OK playing (AppleScript). Search unsupported: {query}"
        return False, msg

    ok, msg = _osascript('tell application "Spotify" to play')
    return ok, msg


def pause() -> Tuple[bool, str]:
    ok, msg = _osascript('tell application "Spotify" to pause')
    return ok, msg


def resume() -> Tuple[bool, str]:
    ok, msg = _osascript('tell application "Spotify" to play')
    return ok, msg


def next_track() -> Tuple[bool, str]:
    script = '''
    try
      tell application "Spotify" to next track
      return "OK next"
    on error errMsg number errNum
      return "ERROR " & errNum & ": " & errMsg
    end try
    '''
    ok, msg = _osascript(script)
    if ok and msg.startswith("ERROR"):
        return False, msg
    return ok, msg
