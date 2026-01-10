from __future__ import annotations

import json
import time
import os
import fcntl
from pathlib import Path
from typing import Any, Dict, List, Optional

from assistant.runtime.app import VeraApp

from v2.engine_adapter import EngineInput, run_engine_via_v1
from v2.runtime_executor import execute_actions
from v2.accountability import apply_declared, apply_receipts
from v2.pds_store import load_pds, save_pds


def _utc_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _today_local_ymd() -> str:
    return time.strftime("%Y-%m-%d", time.localtime())


def _debug_log_path() -> Path:
    return Path("v2") / "_pds" / "_debug" / (_today_local_ymd() + ".log")


def _log_debug(event: str, payload: Dict[str, Any]) -> None:
    try:
        fp = _debug_log_path()
        fp.parent.mkdir(parents=True, exist_ok=True)
        rec = {"utc": _utc_iso(), "event": event, "payload": payload}
        fp.write_text(fp.read_text(encoding="utf-8") + json.dumps(rec, ensure_ascii=False) + "\n", encoding="utf-8") if fp.exists() else fp.write_text(json.dumps(rec, ensure_ascii=False) + "\n", encoding="utf-8")
    except Exception:
        pass




def _lock_file_path() -> Path:
    # Keep lock in debug dir so it never leaks into PDS
    fp = Path("v2") / "_pds" / "_debug" / "vera_v2_bridge.lock"
    fp.parent.mkdir(parents=True, exist_ok=True)
    return fp


def _acquire_single_instance_lock() -> int:
    """
    Hard single-boot guarantee:
    - If another v2 bridge process is running, exit immediately.
    - Ensures exactly one owner of mic + speaker loop.
    Returns an OS-level file descriptor kept open for the process lifetime.
    """
    fp = _lock_file_path()
    fd = os.open(str(fp), os.O_CREAT | os.O_RDWR, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        # Another process holds the lock
        try:
            os.close(fd)
        except Exception:
            pass
        raise SystemExit("VERA v2 bridge already running (lock held). Exiting to prevent duplicate boot/audio.")
    return fd


def _strip_debug_fields(pds: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(pds, dict):
        return {}
    bad = {"last_input_raw", "last_input_utc", "last_output_text"}
    for k in list(pds.keys()):
        if k in bad:
            try:
                del pds[k]
            except Exception:
                pass
    return pds


class VeraAppV2Bridge(VeraApp):
    """
    Month 3 bridge runner:
    - Calls v1 router through v2 boundary (EngineOutput)
    - Executes allowlisted actions via v2.runtime_executor
    - Applies declared actions + receipts into PDS via v2.accountability
    - Persists PDS to disk ONLY when declared/actions/receipts occur (trust contract)
    - Debug telemetry goes to v2/_pds/_debug/YYYY-MM-DD.log (ignored)
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        try:
            self._pds: Dict[str, Any] = load_pds()
        except Exception:
            self._pds = {}

        if not isinstance(self._pds, dict):
            self._pds = {}

        self._pds = _strip_debug_fields(self._pds)

        if "date" not in self._pds:
            self._pds["date"] = _today_local_ymd()

        if "awake" not in self._pds:
            try:
                self._pds["awake"] = bool(getattr(self.store.state, "awake", True))
            except Exception:
                self._pds["awake"] = True

        self._pds_dirty = False

        _log_debug("BOOT", {"date": self._pds.get("date"), "awake": self._pds.get("awake")})

        # Boot-time speech de-dup (prevents double greeting)
        self._boot_utc = time.time()
        self._last_spoken_text = ""
        self._last_spoken_ts = 0.0

    def _persist_if_dirty(self) -> None:
        if not getattr(self, "_pds_dirty", False):
            return
        try:
            save_pds(self._pds)
            self._pds_dirty = False
        except Exception:
            pass



    def speak(self, text: str) -> None:
        """
        Single-boot soft guarantee:
        - Suppress exact duplicate speech within a short window right after boot.
        - Prevents double greeting / repeated init lines without changing normal behavior.
        """
        t = (text or "").strip()
        if not t:
            return

        now = time.time()
        boot_age = now - float(getattr(self, "_boot_utc", now))

        last_t = str(getattr(self, "_last_spoken_text", "") or "")
        last_ts = float(getattr(self, "_last_spoken_ts", 0.0))

        # Only de-dup during early boot window, and only exact duplicates in quick succession
        if boot_age <= 6.0 and t == last_t and (now - last_ts) <= 2.0:
            _log_debug("SPEAK_DEDUP", {"text": t[:120], "boot_age_s": boot_age})
            return

        setattr(self, "_last_spoken_text", t)
        setattr(self, "_last_spoken_ts", now)
        return super().speak(t)

    def process_one(self, raw: str) -> str:
        raw_clean = (raw or "").strip()
        if not raw_clean:
            return ""

        try:
            awake_now = bool(getattr(self.store.state, "awake", True))
        except Exception:
            awake_now = True

        inp = EngineInput(
            raw_text=raw_clean,
            wake_required=bool(getattr(self.cfg, "wake_required", True)),
            priority_enabled=bool(getattr(self.cfg, "priority_enabled", True)),
            awake=awake_now,
            timestamp_utc=_utc_iso(),
            pds=self._pds,
        )

        eng = run_engine_via_v1(inp)

        _log_debug("ENGINE", {"route_kind": eng.route_kind, "actions": eng.actions})

        actions: List[Dict[str, Any]] = eng.actions or []
        if actions:
            try:
                self._pds = apply_declared(self._pds, actions)
                self._pds_dirty = True
            except Exception:
                _log_debug("ERROR", {"where": "apply_declared"})
                pass

        receipts: List[Dict[str, Any]] = []
        if actions:
            try:
                receipts = execute_actions(self, actions)
            except Exception as e:
                receipts = [{"status": "ERROR", "error": repr(e)}]

        if receipts:
            _log_debug("RECEIPTS", {"count": len(receipts)})
            try:
                self._pds = apply_receipts(self._pds, receipts)
                self._pds_dirty = True
            except Exception:
                _log_debug("ERROR", {"where": "apply_receipts"})
                pass

        try:
            self._pds["awake"] = bool(getattr(self.store.state, "awake", True))
        except Exception:
            pass

        self._persist_if_dirty()

        out = super().process_one(raw_clean)

        if out:
            _log_debug("SPOKE", {"len": len(out)})
        return out

    def run(self) -> None:
        try:
            super().run()
        except KeyboardInterrupt:
            _log_debug("EXIT", {"reason": "KeyboardInterrupt"})
            return
def run() -> None:
    # Hard single-instance guard (prevents duplicate greeting/audio init)
    _lock_fd = _acquire_single_instance_lock()
    try:
        app = VeraAppV2Bridge()
        app.run()
    finally:
        try:
            os.close(_lock_fd)
        except Exception:
            pass


if __name__ == "__main__":
    run()

