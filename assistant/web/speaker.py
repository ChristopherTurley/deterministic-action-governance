# assistant/voice/speaker.py
from __future__ import annotations

import os
import sys
import subprocess
import threading
from typing import Optional


class Speaker:
    """
    A blocking TTS speaker.

    Goal: "No matter what, don't turn the mic back on until speaking is done."
    That requires that this class BLOCKS until audio playback finishes.

    Backend selection:
    - Prefer pyttsx3 if installed (offline, blocking via runAndWait()).
    - Fallback to macOS `say` (blocking subprocess).
    """

    def __init__(
        self,
        voice: Optional[str] = None,
        rate: Optional[int] = None,
        volume: Optional[float] = None,
    ) -> None:
        self._lock = threading.RLock()

        # Optional user overrides
        self.voice = voice or os.getenv("VERA_TTS_VOICE", "").strip() or None
        self.rate = rate or _safe_int(os.getenv("VERA_TTS_RATE", "").strip())
        self.volume = volume or _safe_float(os.getenv("VERA_TTS_VOLUME", "").strip())

        # Try initialize pyttsx3 if available
        self._pyttsx3_engine = None
        self._pyttsx3_ok = False
        self._init_pyttsx3()

        # Detect macOS say availability
        self._is_macos = sys.platform == "darwin"

    # -------------------------
    # Public API
    # -------------------------
    def say(self, text: str) -> None:
        """
        Alias to say_blocking, so existing code stays compatible.
        """
        self.say_blocking(text)

    def say_blocking(self, text: str) -> None:
        """
        Blocking: does not return until playback is done.
        """
        t = (text or "").strip()
        if not t:
            return

        with self._lock:
            # Prefer pyttsx3 if initialized
            if self._pyttsx3_ok and self._pyttsx3_engine is not None:
                self._say_pyttsx3_blocking(t)
                return

            # Fallback: macOS 'say'
            if self._is_macos:
                self._say_macos_blocking(t)
                return

            # If neither available, fail loudly with actionable error
            raise RuntimeError(
                "No blocking TTS backend available. "
                "Install pyttsx3 (`pip install pyttsx3`) or run on macOS for built-in `say`."
            )

    # -------------------------
    # Backends
    # -------------------------
    def _init_pyttsx3(self) -> None:
        try:
            import pyttsx3  # type: ignore
        except Exception:
            self._pyttsx3_ok = False
            self._pyttsx3_engine = None
            return

        try:
            engine = pyttsx3.init()
            # Apply optional settings
            if self.rate is not None:
                engine.setProperty("rate", self.rate)
            if self.volume is not None:
                # volume should be 0.0 - 1.0
                engine.setProperty("volume", max(0.0, min(1.0, float(self.volume))))
            if self.voice:
                self._try_set_pyttsx3_voice(engine, self.voice)

            self._pyttsx3_engine = engine
            self._pyttsx3_ok = True
        except Exception:
            self._pyttsx3_ok = False
            self._pyttsx3_engine = None

    def _try_set_pyttsx3_voice(self, engine, desired: str) -> None:
        """
        Attempts to set a voice by matching name/id substring.
        """
        try:
            voices = engine.getProperty("voices") or []
            desired_l = desired.lower()
            for v in voices:
                vid = getattr(v, "id", "") or ""
                vname = getattr(v, "name", "") or ""
                if desired_l in vid.lower() or desired_l in vname.lower():
                    engine.setProperty("voice", vid)
                    return
        except Exception:
            # ignore voice selection errors
            return

    def _say_pyttsx3_blocking(self, text: str) -> None:
        """
        pyttsx3 is blocking if we call runAndWait().
        """
        engine = self._pyttsx3_engine
        if engine is None:
            raise RuntimeError("pyttsx3 engine missing.")

        # Clear queued speech (prevents overlap/backlog)
        try:
            engine.stop()
        except Exception:
            pass

        engine.say(text)
        engine.runAndWait()  # ✅ blocks until finished

    def _say_macos_blocking(self, text: str) -> None:
        """
        macOS `say` blocks until speech is finished.
        """
        cmd = ["say"]
        if self.voice:
            cmd += ["-v", self.voice]
        if self.rate is not None:
            # macOS `say -r` expects words per minute
            cmd += ["-r", str(self.rate)]
        cmd += [text]

        # subprocess.run blocks until finished
        subprocess.run(cmd, check=False)


def _safe_int(s: str) -> Optional[int]:
    try:
        return int(s) if s else None
    except Exception:
        return None


def _safe_float(s: str) -> Optional[float]:
    try:
        return float(s) if s else None
    except Exception:
        return None

