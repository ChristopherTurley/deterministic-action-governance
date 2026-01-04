from __future__ import annotations

from urllib.parse import urlparse, parse_qs, unquote

def _normalize_url(u: str) -> str:
    if not u:
        return u
    u = u.strip()
    if u.startswith("//"):
        u = "https:" + u
    try:
        p = urlparse(u)
        if "duckduckgo.com" in (p.netloc or "") and p.path.startswith("/l/"):
            qs = parse_qs(p.query)
            uddg = qs.get("uddg", [None])[0]
            if uddg:
                real = unquote(uddg)
                if real.startswith("//"):
                    real = "https:" + real
                return real
        return u
    except Exception:
        return u


import re
import time
import webbrowser
from dataclasses import dataclass
from typing import Any, Dict, Optional, List, Tuple

from assistant.router import route_text
from assistant.state.store import StateStore
from assistant.voice.speaker import Speaker
from assistant.voice.listener import VoiceListener

try:
    from assistant.runtime.audio_config import configure_sounddevice
except Exception:
    configure_sounddevice = None  # type: ignore

from assistant.web.web_lookup import search_duckduckgo, spoken_compact, summarize
from assistant.config import DEMO_MODE

def _looks_like_tasks(raw: str) -> bool:
    t = (raw or "").lower()
    if "i need to " in t:
        return True
    if "walk moose at" in t:
        return True
    if t.count(",") >= 1:
        return True
    if " and " in t and ("finish " in t or "outline " in t or "walk " in t or "call " in t):
        return True
    return False

def _is_partial_fragment(raw: str) -> bool:
    t = (raw or "").strip()
    if not t:
        return False
    if len(t) <= 10 and t.endswith("-"):
        return True
    return False

# --- Wake filtering helpers (added) ---
def _norm_text(t: str) -> str:
    return " ".join((t or "").strip().lower().split())

def _is_strict_wake(t: str) -> bool:
    # Accept only clear wake phrases to avoid triggering on lyrics.
    # Examples accepted: "hey vera", "hey vera,", "vera," (only if at start and short)
    nt = _norm_text(t)
    return nt.startswith("hey vera") or nt.startswith("hey, vera") or nt.startswith("hey vera,")

def _mentions_vera(t: str) -> bool:
    nt = _norm_text(t)
    return "vera" in nt
# --- End wake filtering helpers ---

GREET_TEXT = "Welcome back Mister Turley. I have today's rundown ready for you. Say: 'start my day' when you're ready."
MISSION_TEXT = (
    "I'm VERA, a Voice-Enabled Reasoning Assistant. I provide real time dynamic analysis and proactive guidance tailored to your immediate context. "
    "By understanding your voice, screen, and schedule, i ensure you stay focused, organized, and on time throughout your day."
)


@dataclass
class AppConfig:
    wake_required: bool = True
    priority_enabled: bool = True


class VeraApp:
    def __init__(self, *, wake_required: bool = True, priority_enabled: bool = True) -> None:
        self.cfg = AppConfig(wake_required=wake_required, priority_enabled=priority_enabled)
        self.store = StateStore()
        self.speaker = Speaker()
        self.listener = VoiceListener()

        self._last_web_spoken_at: float = 0.0
        self._expecting_tasks: bool = False
        self._tasks: List[Dict[str, Any]] = []
        self._reminders: List[Dict[str, Any]] = []  # {"at": epoch, "msg": str, "fired": bool}

    def speak(self, text: str) -> None:
        try:
            # HARD_SPEAK_LOCKOUT: speak in a blocking way when possible, then lock listening briefly
            try:
                if hasattr(self.speaker, 'say_blocking'):
                    self.speaker.say_blocking(text)
                else:
                    self.speaker.say(text)
            except Exception:
                self.speaker.say(text)
            self._last_spoken_text = text or ''
            self._last_spoken_at = time.time()
            # Note: we intentionally delay re-listening after TTS to prevent self-hearing
            # SELF_TTS_GUARD: mark last spoken text/time so listener can suppress echo
            self._last_spoken_text = text or ''
            self._last_spoken_at = time.time()

        except Exception as e:
            print(f"[AUDIO] speak() failed: {e}")

    def _now_str(self) -> Tuple[str, str]:
        date_str = time.strftime("%A, %B %d, %Y")
        time_str = time.strftime("%I:%M %p").lstrip("0")
        return date_str, time_str

    def _handle_priority_set(self, value: str) -> str:
        self.store.set_priority(value)
        return f"Locked. Your top priority today is: {value}."

    def _handle_priority_get(self) -> str:
        p = self.store.get_priority()
        if not p:
            return "You haven’t set a top priority yet. Say: 'my top priority today is ...'"
        return f"Your top priority is: {p}."

    def _handle_time(self) -> str:
        _, t = self._now_str()
        return f"It’s {t}."

    def _handle_open_link(self, target) -> str:
        import webbrowser

        def _get_links():
            for attr in ("_last_links", "_last_web_links", "_web_links", "_web_results", "_last_web_results", "links"):
                v = getattr(self, attr, None)
                if isinstance(v, list) and v:
                    return v
            st = getattr(self, "store", None)
            if st is not None:
                for attr in ("links", "_last_links", "_last_web_links", "_web_links"):
                    v = getattr(st, attr, None)
                    if isinstance(v, list) and v:
                        return v
                for meth in ("get_links", "last_links", "get_last_links"):
                    fn = getattr(st, meth, None)
                    if callable(fn):
                        try:
                            v = fn()
                            if isinstance(v, list) and v:
                                return v
                        except Exception:
                            pass
                fn = getattr(st, "get", None)
                if callable(fn):
                    try:
                        v = fn("links")
                        if isinstance(v, list) and v:
                            return v
                    except Exception:
                        pass
            return []

        links = _get_links()
        if not links:
            return "I don't have any recent web results. Ask me to search the web first."

        if target == "it":
            idx = 0
        else:
            try:
                idx = int(target) - 1
            except Exception:
                idx = 0

        if idx < 0 or idx >= len(links):
            return f"I only have {len(links)} results. Say open 1, open 2, or open 3."

        item = links[idx] if isinstance(links[idx], dict) else {}
        url = (item.get("url") or item.get("href") or "").strip()
        title = (item.get("title") or item.get("name") or "that result").strip()

        if not url:
            return "That result didn’t include a valid link."

        try:
            url = _normalize_url(url)
        except Exception:
            pass

        try:
            ok = webbrowser.open(url)
        except Exception:
            ok = False

        if ok:
            return f"Opening {title}."
        return "I couldn’t open that link."
    def _handle_web_lookup(self, query: str) -> str:
        now = time.time()
        if now - self._last_web_spoken_at < 3.0:
            self._last_web_spoken_at = now
            return "Still searching—one sec."
        self._last_web_spoken_at = now

        print(f"[WEB] Searching: {query}")
        try:
            results = search_duckduckgo(query, limit=3)
        except Exception as e:
            print("[WEB] search failed:", e)
            return "I couldn't reach the web right now."

        if not results:
            return "No results found."

        items: List[Dict[str, Any]] = []
        for r in results:
            items.append({"title": r.title, "url": r.url, "snippet": r.snippet})
        self.store.set_last_web(items)

        # Terminal print
        print("\n[WEB RESULTS]")
        for i, it in enumerate(items, start=1):
            print(f"{i}. {it['title']}\n   {it['url']}\n")

        # Speak titles cleanly + optional micro-summary
        titles_spoken = spoken_compact(results)
        micro = summarize(query, results)
        if micro:
            return f"{titles_spoken}. {micro} Say: open 1, open 2, or open 3."
        return f"{titles_spoken}. Say: open 1, open 2, or open 3."

    def _handle_spotify(self, meta: Dict[str, Any]) -> str:
        cmd = (meta or {}).get("cmd")
        q = (meta or {}).get("query")

        try:
            import assistant.tools.spotify as sp
        except Exception:
            sp = None  # type: ignore

        if cmd == "liked":
            try:
                from assistant.integrations.spotify_control import spotify_play_liked_from_top
                spotify_play_liked_from_top()
                return "Playing your Liked Songs."
            except Exception:
                try:
                    if sp is not None and hasattr(sp, "liked_songs"):
                        sp.liked_songs()
                        return "Playing your Liked Songs."
                except Exception:
                    pass
                return "Spotify command failed."

        if cmd == "pause":
            try:
                if sp is not None and hasattr(sp, "pause"):
                    sp.pause()
                return "Paused."
            except Exception:
                return "Spotify command failed."

        if cmd == "resume":
            try:
                if sp is not None and hasattr(sp, "resume"):
                    sp.resume()
                    return "Playing."
                if sp is not None and hasattr(sp, "play"):
                    sp.play("")
                    return "Playing."
                return "Spotify integration is not available."
            except Exception:
                return "Spotify command failed."

        if cmd == "play":
            try:
                if sp is not None and hasattr(sp, "play"):
                    sp.play(str(q or "").strip())
                    return f"Playing: {q}."
                return "Spotify integration is not available."
            except Exception:
                return "Spotify command failed."

        if cmd == "next":
            try:
                if sp is not None and hasattr(sp, "next_track"):
                    sp.next_track()
                    return "Next."
                return "Spotify integration is not available."
            except Exception:
                return "Spotify command failed."

        if cmd == "previous":
            try:
                if sp is not None and hasattr(sp, "previous_track"):
                    sp.previous_track()
                    return "Previous."
                return "Spotify integration is not available."
            except Exception:
                return "Spotify command failed."

        return "Spotify command failed."

    # -------- Phase 1 planning / reminders --------

    def _parse_time_today(self, text: str) -> Optional[float]:
        """
        Parse times like:
          3pm, 3 pm, 3:15pm, 15:30
        Returns epoch seconds for today local time.
        """
        s = (text or "").lower()

        m = re.search(r"\b(\d{1,2})(?::(\d{2}))?\s*(am|pm)\b", s)
        if m:
            hh = int(m.group(1))
            mm = int(m.group(2) or "0")
            ap = m.group(3)
            if hh == 12:
                hh = 0
            if ap == "pm":
                hh += 12
            now = time.localtime()
            t = time.struct_time((now.tm_year, now.tm_mon, now.tm_mday, hh, mm, 0, now.tm_wday, now.tm_yday, now.tm_isdst))
            return time.mktime(t)

        m2 = re.search(r"\b(\d{1,2}):(\d{2})\b", s)
        if m2:
            hh = int(m2.group(1))
            mm = int(m2.group(2))
            now = time.localtime()
            t = time.struct_time((now.tm_year, now.tm_mon, now.tm_mday, hh, mm, 0, now.tm_wday, now.tm_yday, now.tm_isdst))
            return time.mktime(t)

        return None

    def _add_reminder(self, when_epoch: float, msg: str) -> None:
        if when_epoch <= time.time():
            return
        self._reminders.append({"at": when_epoch, "msg": msg, "fired": False})
        self._reminders.sort(key=lambda x: x["at"])

    def _tick_reminders(self) -> None:
        now = time.time()
        fired_any = False
        for r in self._reminders:
            if not r["fired"] and now >= float(r["at"]):
                r["fired"] = True
                fired_any = True
                self.speak(str(r["msg"]))
                print(f"VERA: {r['msg']}")
        if fired_any:
            # Keep list from growing forever
            self._reminders = [x for x in self._reminders if not x["fired"]]

    def _capture_tasks(self, raw: str) -> str:

        # NORMALIZE_DOTTED_AMPM: allow '11 p.m.' / '7 a.m.' formats for time parsing

        try:

            raw = re.sub(r"\b([ap])\.\s*m\.\b", r"\1m", raw, flags=re.IGNORECASE)

            raw = re.sub(r"\b([ap])\.\s*m\b", r"\1m", raw, flags=re.IGNORECASE)

        except Exception:

            pass

        # --- Phase C micro-patch: patient _capture_tasks (v4) ---
        raw0 = raw or ''
        # --- Phase C micro-patch: time normalization (dot-time + ordinals) ---
        # ASR fixes: '4th' -> '4', '4.30pm' -> '4:30 pm', '4.30 p.m.' -> '4:30 pm'
        raw0 = re.sub(r'\bat\s+(\d{1,2})th\b', r'at \1', raw0, flags=re.IGNORECASE)
        raw0 = re.sub(r'\b(\d{1,2})\.(\d{2})\s*(a\.?m\.?|p\.?m\.?)\b', r'\1:\2 \3', raw0, flags=re.IGNORECASE)
        raw0 = re.sub(r'\b(\d{1,2})\.(\d{2})\b', r'\1:\2', raw0)
        # --- end time normalization ---
        try:
            from assistant.router.core import _strip_wake as _sw
            _hw, _rest = _sw(raw0)
            if _hw:
                raw0 = _rest
        except Exception:
            pass
        raw0 = re.sub(r'^\s*hey\s*[, ]+\s*vera\b[\s,]*', '', raw0, flags=re.IGNORECASE)
        raw0 = re.sub(r'^\s*vera\b[\s,]*', '', raw0, flags=re.IGNORECASE)
        s = (raw0 or '').strip()
        low = s.lower().strip(' \t\r\n.,!?;:')
        if low == '' or low in ('!', '?', '.', ',', '...'):
            return "Go ahead — I’m listening."
        if re.match(r'^(my\s+)?tasks(\s+today)?\s+are\s*$', low):
            return "Go ahead — tell me your tasks. You can say them slowly."
        if low in ('my tasks', 'tasks', 'my tasks today', 'tasks today'):
            return "Go ahead — tell me the tasks. Times are optional."
        if s.endswith('?') and ('task' in low) and len(low.split()) <= 8:
            return "Go ahead — tell me your tasks when you’re ready."
        # If trailing ellipsis but a time is present, don't block processing
        if s.endswith('...') and (not re.search(r"\bat\s+\d", low)):
            return "Go ahead — I’m listening."
        # --- end patient _capture_tasks (v4) ---
        # --- Phase C micro-patch: intake cancel + pending-time (v6) (inside _capture_tasks) ---
        s_in = (raw or '').strip()
        low_in = s_in.lower().strip(' \t\r\n.,!?;:')
        
        # If user repeats assistant filler, don't treat it as a task
        if low_in in ('go ahead', 'go ahead.', 'go ahead!', 'take your time', 'take your time.', 'yes', 'yeah', 'yep'):
            return "Go ahead — tell me the full task list."
        
        # If user says something clearly not a task list during intake, prompt again (prevents 'you got this' getting captured)
        if re.search(r'\b(you got this|that\s*is\s*all|thats all|that\'s all|just testing|test)\b', low_in):
            return "Tell me your tasks for today (commas are fine)."
        
        # Pending time assignment: if we previously asked for a time, accept '<task> at <time>' now
        pending = getattr(self, '_pending_time_for', None)
        m = re.match(r'^(.+?)\s+at\s+(.+)$', low_in)
        if pending and m:
            tname = m.group(1).strip()
            ttime = m.group(2).strip()
            # Phase C micro-patch: extract first time token (v1)
            # If ASR appends extra words/fragments, keep only the first time expression
            mtime = re.search(r"(\d{1,2}(:\d{2})?\s*(a\.?m\.?|p\.?m\.?))", ttime)
            if mtime:
                ttime = mtime.group(1)

            # Only apply if user is answering the pending task (contains the pending name)
            if pending in tname:
                applied = False
                # Try a few common storage shapes safely
                try:
                    st = getattr(self.store, 'state', None)
                    tasks = None
                    if st is not None and hasattr(st, 'tasks'):
                        tasks = st.tasks
                    elif hasattr(self.store, 'tasks'):
                        tasks = self.store.tasks
                    if isinstance(tasks, list):
                        for item in tasks:
                            if isinstance(item, dict):
                                txt = str(item.get('text','')).lower()
                                if pending in txt and not item.get('time'):
                                    item['time'] = ttime
                                    applied = True
                                    break
                            else:
                                # string task list fallback: can't safely set time
                                pass
                except Exception:
                    pass
                setattr(self, '_pending_time_for', None)
                if applied:
                    return f"Locked. {tname.title()} at {ttime}. Want me to build a focused schedule? Say: 'build my schedule'."
                # If we couldn't apply, fall back to accepting it as-is (better than looping forever)
                return f"Got it: {tname} at {ttime}. Want me to build a focused schedule? Say: 'build my schedule'."
        # --- end v6 ---
        # --- Phase C micro-patch: intake completeness guard (v5) ---
        # If ASR returns a fragment, do NOT lock tasks yet.
        frag = (raw0 if 'raw0' in locals() else (raw or '')).strip()
        frag_low = frag.lower().strip(' \t\r\n.,!?;:')
        # Very short fragments (e.g. 'my task') are almost never a complete list
        if len(frag_low.split()) < 4:
            return "Go ahead — keep going. Tell me the full task list."
        # If it looks like a lead-in without any list structure, keep listening
        has_list_signals = any(x in frag for x in [',', ' and ', ';']) or bool(re.search(r'\b(at|by)\s+\d', frag_low))
        if (('task' in frag_low) or frag_low.startswith('my tasks')) and (not has_list_signals) and len(frag_low.split()) < 7:
            return "Go ahead — tell me the tasks (you can separate them with commas)."
        # --- end intake completeness guard (v5) ---
        # --- Phase C micro-patch: patient task intake (wake strip + lead-in) ---
        # Strip wake phrase during task intake so parsing is consistent
        try:
            from assistant.router.core import _strip_wake as _sw
            _hw, _rest = _sw(raw)
            if _hw:
                raw = _rest
        except Exception:
            pass

        _raw0 = (raw or '').strip()
        _low0 = _raw0.lower().strip(' \t\r\n.,!?;:')
        # Treat short lead-ins / questions as 'still talking' (do NOT capture yet)
        if re.match(r'^(my\s+)?tasks(\s+today)?\s+are\s*$', _low0):
            return "Take your time — I’m listening. Tell me your tasks (times optional)."
        if _raw0.endswith('?') and len(_low0.split()) <= 5 and 'task' in _low0:
            return "Tell me the tasks when you’re ready — you can say them naturally, even slowly."
        if _raw0.endswith('...'):
            return "Go ahead — I’m listening."
        # --- end micro-patch ---
        """
        Phase 1 simple intake:
        - Supports comma-separated tasks
        - Detects timed tasks like "walk my dog at 3pm"
        - Adds reminders 10 min + 2 min before
        """
        text = (raw or "").strip()
        # Phase C micro-patch: strip task-intake lead-in (v1)
        text = re.sub(r"^\s*(my\s+)?tasks(\s+today)?\s+are\s+", "", text, flags=re.IGNORECASE)
        # --- end micro-patch ---
        # Phase C micro-patch: add-task lead-in normalize (v1)
        # Allow natural phrasing: 'add task ...', 'new task ...', 'add ... to my tasks'
        text = re.sub(r'^\s*(hey\s+vera\s*,?\s*)?', '', text, flags=re.IGNORECASE)
        text = re.sub(r'^\s*(add\s+(a\s+)?)?task\s*[:\-]?\s*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'^\s*new\s+task\s*[:\-]?\s*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'^\s*add\s+(.+)\s+to\s+my\s+tasks\s*[:\-]?\s*', r'\1', text, flags=re.IGNORECASE)
        # --- end micro-patch ---
        if not text:
            return "Tell me your tasks for today. Example: finish Phase 1, create UI, walk Moose at 3pm."

        # Split tasks by comma
        parts = [p.strip() for p in re.split(r",|\sand\s|;|\sthen\s|\snext\s", text, flags=re.IGNORECASE) if p.strip()]  # Phase C micro-patch: improved splitter (v1)
        added = 0

        for p in parts:
            when = self._parse_time_today(p)
            task = {"text": p, "time": when}
            self._tasks.append(task)
            added += 1

            if when:
                # 10 min and 2 min reminders
                self._add_reminder(when - 10 * 60, f"Hey Mister Turley — you’re 10 minutes out from: {p}.")
                self._add_reminder(when - 2 * 60, f"Hey Mister Turley — you’re 2 minutes out from: {p}.")

        # If any mentions Moose/dog without time, prompt for time
        if any(("walk" in t["text"].lower()) and not t["time"] for t in self._tasks):
            self._pending_time_for = 'walk moose'
            return f"Locked {added} tasks. What time do you want to walk Moose? Say: 'walk Moose at 3pm'."

        return f"Locked {added} tasks. Want me to build a focused schedule for these? Say: 'build my schedule'."

    def _build_schedule(self) -> str:
        p = self.store.get_priority() or "your top priority"
        timed = [t for t in self._tasks if t.get("time")]
        untimed = [t for t in self._tasks if not t.get("time")]

        # Very simple schedule suggestion
        lines = []
        if timed:
            lines.append("Anchored items:")
            for t in sorted(timed, key=lambda x: x["time"]):
                tm = time.strftime("%I:%M %p", time.localtime(float(t["time"]))).lstrip("0")
                lines.append(f"- {tm}: {t['text']}")

        if untimed:
            lines.append("Focus blocks (suggested order):")
            lines.append(f"- Block 1 (90m): {p}")
            for i, t in enumerate(untimed, start=2):
                lines.append(f"- Block {i} (60m): {t['text']}")

        if not lines:
            return "You don’t have any tasks saved yet. Tell me your tasks for today."

        return "Here’s a focused plan. " + " ".join(lines)


    # --- Phase B micro-patch: mission -> capabilities list ---
    def _mission_capabilities(self) -> str:
        return (
            "Here’s what I can do in VERA v1:\n"
            "- Start your day: say 'start my day' to begin task intake.\n"
            "- Capture tasks: give tasks with times (e.g., 'walk Moose at 3pm').\n"
            "- Top priority: set/get your priority ('my top priority today is ...').\n"
            "- Build a simple schedule: say 'build my schedule'.\n"
            "- Time: ask 'what time is it'.\n"
            "- Sleep/Wake: say 'go to sleep' and 'hey vera' to wake me.\n"
            "- Web lookup (if enabled): ask a question and I can look it up.\n"
            "- Spotify (if enabled): play/pause/resume/search."
        )
    # --- end micro-patch ---
    # -------- routing --------

    def process_one(self, raw: str) -> str:
        # If we're in task-intake mode, temporarily disable wake requirement
        wake_required = self.cfg.wake_required
        if self._expecting_tasks:
            wake_required = False

        r = route_text(
            raw,
            wake_required=wake_required,
            priority_enabled=self.cfg.priority_enabled,
            awake=self.store.state.awake,
        )
        kind = getattr(r, "kind", "LLM_FALLBACK")
        meta = getattr(r, "meta", {}) or {}
        cleaned = getattr(r, "cleaned", "")

        # Handle task intake (phase 1)
        if self._expecting_tasks and kind in ("LLM_FALLBACK", "NUDGE_WAKE"):
            # --- Phase C micro-patch: intake cancel + pending-time (v6) ---
            _r0 = (raw or '').strip().lower().strip(' \t\r\n.,!?;:')
            if _r0 in ('cancel', 'never mind', 'nevermind', 'stop', 'stop intake', 'exit', 'quit', 'bye', 'bye now', 'goodbye'):
                self._expecting_tasks = False
                return "Okay — canceled task intake."
            resp = self._capture_tasks(raw)
            # Stay in intake mode for patience prompts
            if isinstance(resp, str) and resp.startswith(('Take your time', 'Go ahead')):
                return resp
            # Stay in intake mode when asking for missing time
            if isinstance(resp, str) and ('What time do you want' in resp):
                return resp
            self._expecting_tasks = False
            return resp
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
        # Phase C micro-patch: remove spoken example tasks (v1)
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

        # Manual planner commands
        c = (cleaned or "").lower().strip().strip(".,!?;:")
        if c in ("build my schedule", "build schedule", "make my schedule", "plan my day", "create my schedule"):
            return self._build_schedule()

        # Phase C micro-patch: allow add-task outside intake (v1)
        lc = (cleaned or '').lower().strip()
        if kind == 'LLM_FALLBACK':
            if re.match(r"^add\s+(a\s+)?task\b", lc) or lc.startswith('new task') or re.search(r"\badd\b.+\bto\s+my\s+tasks\b", lc):
                return self._capture_tasks(raw)
        # --- end micro-patch ---

        return "Ask me directly — I’ll answer."

    def run(self) -> None:
        if configure_sounddevice is not None:
            configure_sounddevice()

        print(f"VERA: {GREET_TEXT}")
        self.speak(GREET_TEXT)

        while True:
            # Reminders tick before listening
            self._tick_reminders()

            if not DEMO_MODE:
                print("[STAGE] LISTEN")
            # --- Phase C micro-patch: listener patience by mode (v1) ---
            # During task intake or pending-time follow-up, require a longer pause before cut-off
            _in_intake = bool(getattr(self, '_expecting_tasks', False) or getattr(self, '_pending_time_for', None))
            try:
                if _in_intake:
                    self.listener.silence_hold_sec = 0.90
                    self.listener.hangover_sec = 0.35
                    # Also require a minimum amount of speech before we allow endpointing
                    self.listener.min_speech_sec = 1.25 if _in_intake else 0.60
                    # Slightly relax silence threshold during intake to prevent slow-speech chop
                    self.listener.silence_relax = 0.85 if _in_intake else 1.00
                else:
                    self.listener.silence_hold_sec = 0.55
                    self.listener.hangover_sec = 0.25
            except Exception:
                pass
            # --- end micro-patch ---
            raw = (self.listener.listen() or "").strip()
            # HARD_SPEAK_LOCKOUT: never accept mic input immediately after VERA speaks
            # This prevents TTS -> mic bleed from being treated as user speech.
            try:
                _lsa = float(getattr(self, '_last_spoken_at', 0.0))
                # 1.25s cooldown is intentional; it will drop any speech-over-TTS.
                if raw and _lsa and (time.time() - _lsa) < 1.25:
                    raw = ''
            except Exception:
                pass

            # Phase C micro-patch: echo suppression (v1)
            # Drop mic input that matches what VERA just spoke (speaker -> mic bleed)
            # v2: This belongs in an audio adapter; v1: keep it conservative but robust
            try:
                if raw and hasattr(self, '_last_spoken_at'):
                    if time.time() - float(getattr(self, '_last_spoken_at', 0)) < 4.0:
                        def _norm(x):
                            x = (x or '').lower()
                            x = re.sub(r'\s+', ' ', x)
                            x = x.strip(' \t\r\n.,!?;:')
                            return x
                        def _tokset(x):
                            x = _norm(x)
                            # keep words and digits chunks (handles "804pm" variations)
                            toks = re.findall(r"[a-z0-9']+", x)
                            return set(toks)

                        n_raw = _norm(raw)
                        n_last = _norm(getattr(self, '_last_spoken_text','') or '')

                        # Fast path: substring containment
                        if n_raw and n_last and (n_raw in n_last or n_last in n_raw):
                            raw = ''

                        # Robust path: token overlap similarity
                        if raw:
                            a = _tokset(raw)
                            b = _tokset(getattr(self, '_last_spoken_text','') or '')
                            if a and b:
                                overlap = len(a & b) / float(min(len(a), len(b)))
                                # If most of the smaller set overlaps, it's almost certainly self-echo
                                if overlap >= 0.65:
                                    raw = ''
            except Exception:
                pass
            # --- end echo suppression ---


            # --- Wake gate tuning: silently ignore background audio/lyrics ---
            # Do not respond or route when wake is required and wake phrase is missing.
# --- Phase C micro-patch: disable strict wake gate during task intake ---
            if getattr(self.cfg, 'wake_required', True) and (not getattr(self, '_expecting_tasks', False)) and raw:
                if not _is_strict_wake(raw):
                    raw = ''
            # --- end micro-patch ---
            # --- End wake gate tuning ---
            if not raw:
                continue
            print(f"[RAW] {raw}")
            print(f"USER: {raw}")

            # Demo polish: accept task intake without forcing the user to say 'start my day' first
            if _is_partial_fragment(raw):
                raw = ""
            
            out = (self.process_one(raw) or "").strip()
            if raw and _looks_like_tasks(raw) and "Ask me directly" in out:
                # Auto-enter daily brief flow once, then retry original utterance
                _ = (self.process_one("start my day") or "").strip()
                out = (self.process_one(raw) or "").strip()
            if out:
                print(f"VERA: {out}")
                self.speak(out)

            # Reminders tick after processing
            self._tick_reminders()


def run() -> None:
    VeraApp().run()
