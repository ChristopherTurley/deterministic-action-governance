from __future__ import annotations

import time
import re
from typing import Any, Dict

from assistant.runtime.app import VeraApp, configure_sounddevice, GREET_TEXT, DEMO_MODE
from v2.engine_adapter import EngineInput, run_engine_via_v1


class VeraAppV2Bridge(VeraApp):
    """
    Month 3 bridge runner:
    - DOES NOT modify v1
    - Uses v2 boundary adapter (which calls v1 router)
    - Executes using existing VeraApp underscore handlers
    - Keeps runtime loop behavior identical (inherits VeraApp.run)
    """

    def process_one(self, raw: str) -> str:
        # Preserve current runtime wake override policy exactly
        wake_required = self.cfg.wake_required
        if getattr(self, "_expecting_tasks", False):
            wake_required = False

        try:
            _fu = float(getattr(self, "_followup_until", 0.0))
            if _fu and (time.time() < _fu):
                wake_required = False
        except Exception:
            pass

        # v2 boundary: calls v1 route_text internally
        inp = EngineInput(
            raw_text=str(raw or ""),
            wake_required=bool(wake_required),
            priority_enabled=bool(self.cfg.priority_enabled),
            awake=bool(getattr(self.store.state, "awake", True)),
            timestamp_utc=None,
            context={
                "expecting_tasks": bool(getattr(self, "_expecting_tasks", False)),
                "followup_mode": (getattr(self, "_followup_mode", None)),
                "followup_active": bool(
                    float(getattr(self, "_followup_until", 0.0)) and (time.time() < float(getattr(self, "_followup_until", 0.0)))
                ),
            },
            pds=None,
        )
        out = run_engine_via_v1(inp)

        kind = str(getattr(out, "route_kind", "") or "LLM_FALLBACK")
        debug = getattr(out, "debug", {}) or {}
        meta = debug.get("meta", {}) if isinstance(debug, dict) else {}
        if not isinstance(meta, dict):
            meta = {}

        # Recompute cleaned/cmd locally for the few runtime-only manual commands
        # (no v1 edits; safe import of existing helpers)
        cleaned = ""
        cmd = ""
        try:
            import assistant.router.core as v1_core
            has_wake, stripped = v1_core._strip_wake(raw)  # type: ignore[attr-defined]
            cleaned = v1_core._norm(stripped)              # type: ignore[attr-defined]
            cmd = v1_core._cmd(cleaned)                    # type: ignore[attr-defined]
        except Exception:
            cleaned = (raw or "").strip().lower()
            cleaned = re.sub(r"\s+", " ", cleaned)
            cmd = cleaned.strip(" \t\r\n.,!?;:")

        # --- Task intake handling (preserve current behavior) ---
        if getattr(self, "_expecting_tasks", False) and kind in ("LLM_FALLBACK", "NUDGE_WAKE"):
            _r0 = (raw or "").strip().lower().strip(" \t\r\n.,!?;:")
            if _r0 in (
                "cancel", "never mind", "nevermind", "stop", "stop intake",
                "exit", "quit", "bye", "bye now", "goodbye",
            ):
                self._expecting_tasks = False
                return "Okay — canceled task intake."

            resp = self._capture_tasks(raw)

            # FOLLOWUP_WINDOW_V1 parity: after locking tasks, allow immediate schedule build without wake
            try:
                if isinstance(resp, str) and resp.startswith("Locked"):
                    self._followup_until = time.time() + 25.0
            except Exception:
                pass

            if isinstance(resp, str) and resp.startswith(("Take your time", "Go ahead")):
                return resp
            if isinstance(resp, str) and ("What time do you want" in resp):
                return resp

            self._expecting_tasks = False
            return resp
        # --- End intake handling ---

        # --- Kind handling (mapped 1:1 to current process_one) ---
        if kind == "ASLEEP_IGNORE":
            return ""
        if kind == "WAKE":
            self.store.wake()
            return "Yes?"
        if kind == "NUDGE_WAKE":
            return "Say 'Hey Vera' first, then ask your question."
        if kind == "SLEEP":
            self.store.sleep()
            return "Going to sleep. Say 'Hey Vera' to wake me."
        if kind == "MISSION":
            return self._mission_capabilities()
        if kind == "TIME":
            return self._handle_time()
        if kind == "START_DAY":
            date_str, time_str = self._now_str()
            p = self.store.get_priority()
            priority_line = f"Top priority: {p}." if p else "You haven’t set a top priority yet."
            self._expecting_tasks = True
            return f"Today is {date_str}. It’s {time_str}. {priority_line} Tell me your tasks for today—include times if you can."
        if kind == "SCREEN_SUMMARY":
            return "Screen summary is not available yet."
        if kind == "OPEN_LINK":
            return self._handle_open_link(meta.get("target"))
        if kind == "PRIORITY_SET":
            return self._handle_priority_set(str(meta.get("value", "")).strip())
        if kind == "PRIORITY_GET":
            return self._handle_priority_get()
        if kind == "WEB_LOOKUP":
            q = str(meta.get("query", cleaned)).strip()
            return self._handle_web_lookup(q)
        if kind == "SPOTIFY":
            return self._handle_spotify(meta)

        # Manual planner commands (runtime-only, same as today)
        c = (cleaned or "").lower().strip().strip(".,!?;:")
        if c in ("build my schedule", "build schedule", "make my schedule", "plan my day", "create my schedule"):
            return self._build_schedule()

        # Allow add-task outside intake (parity)
        lc = (cleaned or "").lower().strip()
        if kind == "LLM_FALLBACK":
            if re.match(r"^add\s+(a\s+)?task\b", lc) or lc.startswith("new task") or re.search(r"\badd\b.+\bto\s+my\s+tasks\b", lc):
                return self._capture_tasks(raw)

        return "Ask me directly — I’ll answer."


def run() -> None:
    # Keep entry behavior consistent
    if configure_sounddevice is not None:
        configure_sounddevice()

    print(f"VERA: {GREET_TEXT}")
    app = VeraAppV2Bridge()
    app.speak(GREET_TEXT)
    app.run()


if __name__ == "__main__":
    run()
