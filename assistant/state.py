from __future__ import annotations
import time

class AudioGate:
    """
    Simple half-duplex audio gate.
    When closed, we skip listening to avoid VERA hearing herself.
    """

    def __init__(self) -> None:
        self._closed_until = 0.0

    def open_for(self, ms: int) -> None:
        """Close the gate for ms milliseconds from now."""
        self._closed_until = max(self._closed_until, time.time() + (ms / 1000.0))

    def is_closed(self) -> bool:
        return time.time() < self._closed_until

