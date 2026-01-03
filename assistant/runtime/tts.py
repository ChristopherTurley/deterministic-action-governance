from __future__ import annotations
import subprocess
import shlex

def speak_mac_say(text: str) -> bool:
    """
    macOS 'say' TTS. Returns True if it ran without error.
    """
    t = (text or "").strip()
    if not t:
        return True
    try:
        # -r rate (optional). Remove if you want default speed.
        subprocess.run(["say", "-r", "190", t], check=True)
        return True
    except Exception:
        return False


def speak(text: str) -> None:
    """
    Single entrypoint used by app.py.
    """
    ok = speak_mac_say(text)
    if not ok:
        # last-resort fallback: don't crash, but you still see output
        print(f"[TTS_FAIL] {text}")
