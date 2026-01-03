import subprocess

def _run_osascript(script: str) -> str:
    p = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    out = (p.stdout or "").strip()
    err = (p.stderr or "").strip()
    if p.returncode != 0:
        raise RuntimeError(err or out or f"osascript failed ({p.returncode})")
    return out

def spotify_player_state() -> str:
    # returns: playing | paused | stopped
    return _run_osascript('tell application "Spotify" to get player state')

def spotify_play_liked_from_top() -> None:
    _run_osascript(
        'tell application "Spotify"\n'
        '  set shuffling to false\n'
        '  play track "spotify:collection"\n'
        '  set player position to 0\n'
        'end tell'
    )

def spotify_play_query(query: str) -> None:
    # Your existing query play may be different; keep this if you're using AppleScript search later.
    # For now, just "play" resumes.
    _run_osascript('tell application "Spotify" to play')

def spotify_pause() -> None:
    _run_osascript('tell application "Spotify" to pause')

def spotify_resume() -> None:
    _run_osascript('tell application "Spotify" to play')

def spotify_next() -> None:
    _run_osascript('tell application "Spotify" to next track')
