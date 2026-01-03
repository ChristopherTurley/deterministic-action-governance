from __future__ import annotations

import subprocess
from typing import Optional


class Speaker:
    """
    macOS 'say' wrapper.
    Critical details:
    - Always pass '--' before message so messages starting with '-' don't become flags.
    - Provide say_blocking() for deterministic turn-taking.
    """

    def __init__(self, voice: Optional[str] = None) -> None:
        self.voice = voice

    def _cmd(self, text: str):
        text = (text or "").strip()
        if not text:
            return None
        if self.voice:
            return ["say", "-v", self.voice, "--", text]
        return ["say", "--", text]

    def say_blocking(self, text: str) -> None:
        cmd = self._cmd(text)
        if not cmd:
            return
        proc = subprocess.Popen(cmd)
        proc.wait()

    def say(self, text: str) -> None:
        cmd = self._cmd(text)
        if not cmd:
            return
        subprocess.Popen(cmd)
