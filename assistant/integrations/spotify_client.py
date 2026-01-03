from __future__ import annotations

import os
import subprocess
import urllib.parse
from dataclasses import dataclass
from typing import Optional, Tuple


def _osascript(script: str) -> subprocess.CompletedProcess:
    return subprocess.run(["osascript", "-e", script], text=True, capture_output=True)


def _spotify_app_installed() -> bool:
    return os.path.exists("/Applications/Spotify.app") or os.path.exists(os.path.expanduser("~/Applications/Spotify.app"))


@dataclass
class SpotifyClientConfig:
    duck_target_volume: int = 12


class SpotifyClient:
    """
    APP-ONLY Spotify client (V1 stable mode):
    - Never opens browser
    - Never uses Spotify Web API (OAuth opens browser)
    - Uses AppleScript to activate + open search + play/pause
    """

    def __init__(self, config: Optional[SpotifyClientConfig] = None) -> None:
        self.config = config or SpotifyClientConfig()

    @property
    def app_available(self) -> bool:
        return _spotify_app_installed()

    # ---------- App controls ----------
    def open_app(self) -> Tuple[bool, str]:
        p = subprocess.run(["open", "-a", "Spotify"], text=True, capture_output=True)
        if p.returncode != 0:
            return False, (p.stderr or p.stdout or "").strip() or "Failed to open Spotify app."
        return True, ""

    def activate_app(self) -> None:
        _osascript('tell application "Spotify" to activate')

    def open_location_app(self, uri: str) -> Tuple[bool, str]:
        u = (uri or "").strip()
        if not u.startswith("spotify:"):
            return False, "Not a spotify: URI."

        script = f'''
tell application "Spotify"
  activate
  try
    open location "{u}"
    return "OK"
  on error errMsg number errNum
    return "ERR:" & errNum & ":" & errMsg
  end try
end tell
'''
        p = _osascript(script)
        out = (p.stdout or "").strip()
        if out.startswith("ERR:"):
            return False, out
        return True, ""

    def play(self) -> Tuple[bool, str]:
        script = r'''
tell application "Spotify"
  try
    play
    return "OK"
  on error errMsg number errNum
    return "ERR:" & errNum & ":" & errMsg
  end try
end tell
'''
        p = _osascript(script)
        out = (p.stdout or "").strip()
        return (not out.startswith("ERR:")), out if out.startswith("ERR:") else ""

    def pause(self) -> Tuple[bool, str]:
        script = r'''
tell application "Spotify"
  try
    pause
    return "OK"
  on error errMsg number errNum
    return "ERR:" & errNum & ":" & errMsg
  end try
end tell
'''
        p = _osascript(script)
        out = (p.stdout or "").strip()
        return (not out.startswith("ERR:")), out if out.startswith("ERR:") else ""

    def is_playing(self) -> bool:
        script = r'''
tell application "Spotify"
  if it is running then
    try
      return (player state as string)
    on error
      return "stopped"
    end try
  else
    return "stopped"
  end if
end tell
'''
        p = _osascript(script)
        state = (p.stdout or "").strip().lower()
        return "playing" in state

    def get_volume(self) -> Optional[int]:
        script = r'''
tell application "Spotify"
  try
    return (sound volume as integer)
  on error
    return ""
  end try
end tell
'''
        p = _osascript(script)
        out = (p.stdout or "").strip()
        try:
            return int(out)
        except Exception:
            return None

    def set_volume(self, vol: int) -> None:
        v = max(0, min(100, int(vol)))
        script = f'''
tell application "Spotify"
  try
    set sound volume to {v}
  end try
end tell
'''
        _osascript(script)

    def duck_volume(self, target: Optional[int] = None) -> Optional[int]:
        tgt = self.config.duck_target_volume if target is None else int(target)
        prev = self.get_volume()
        if prev is None:
            return None
        self.set_volume(tgt)
        return prev

    def restore_volume(self, prev: Optional[int]) -> None:
        if prev is None:
            return
        self.set_volume(prev)

    # ---------- Unified action ----------
    def search_and_play(self, query: str, prefer: Optional[str] = None) -> Tuple[bool, str]:
        """
        V1 behavior:
        - Open Spotify app
        - Open search page inside app
        - Best-effort play (may resume last if nothing queued)
        """
        if not self.app_available:
            return False, "Spotify desktop app is not installed."

        q = (query or "").strip() or "lofi work music"

        ok, err = self.open_app()
        if not ok:
            return False, err

        self.activate_app()

        search_uri = "spotify:search:" + urllib.parse.quote(q)
        ok2, err2 = self.open_location_app(search_uri)
        if not ok2:
            return False, f"Spotify app couldn't open search: {err2}"

        ok3, err3 = self.play()
        if ok3:
            return True, ""
        return True, "Opened Spotify search in app. Hit Play if nothing queued."

