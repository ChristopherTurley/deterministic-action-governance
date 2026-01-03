from __future__ import annotations
import subprocess

def _osa(cmd: str) -> str:
    p = subprocess.run(["osascript", "-e", cmd], capture_output=True, text=True)
    return (p.stdout or "").strip()

def spotify_set_volume(vol: int) -> None:
    vol = max(0, min(100, int(vol)))
    _osa(f'tell application "Spotify" to set sound volume to {vol}')

def spotify_get_volume() -> int:
    out = _osa('tell application "Spotify" to get sound volume')
    try:
        return int(out)
    except Exception:
        return 50

def spotify_is_running() -> bool:
    out = _osa('tell application "System Events" to (name of processes) contains "Spotify"')
    return out.lower() == "true"
