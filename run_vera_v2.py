from __future__ import annotations

import time
from typing import Any, Dict

from assistant.runtime.app import VeraApp

from v2.pds_store import load_pds, save_pds


class VeraAppV2Bridge(VeraApp):
    """
    Month 3 bridge runner:
    - Does NOT modify v1.
    - Ensures PDS is loaded/saved deterministically to v2/_pds/YYYY-MM-DD.json.
    - Keeps runtime behavior intact (delegates to v1 VeraApp.process_one for speech/handlers).
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        try:
            self._pds: Dict[str, Any] = load_pds()
        except Exception:
            self._pds = {}

        if not isinstance(self._pds, dict):
            self._pds = {}

        if "date" not in self._pds:
            self._pds["date"] = time.strftime("%Y-%m-%d", time.localtime())

        if "awake" not in self._pds:
            try:
                self._pds["awake"] = bool(getattr(self.store.state, "awake", True))
            except Exception:
                self._pds["awake"] = True

        try:
            save_pds(self._pds)
        except Exception:
            pass

    def process_one(self, raw: str) -> str:
        try:
            self._pds["last_input_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            self._pds["last_input_raw"] = (raw or "").strip()
            try:
                self._pds["awake"] = bool(getattr(self.store.state, "awake", True))
            except Exception:
                pass
            save_pds(self._pds)
        except Exception:
            pass

        out = super().process_one(raw)

        try:
            self._pds["last_output_text"] = (out or "").strip()
            try:
                self._pds["awake"] = bool(getattr(self.store.state, "awake", True))
            except Exception:
                pass
            save_pds(self._pds)
        except Exception:
            pass

        return out


def run() -> None:
    app = VeraAppV2Bridge()
    app.run()


if __name__ == "__main__":
    run()
