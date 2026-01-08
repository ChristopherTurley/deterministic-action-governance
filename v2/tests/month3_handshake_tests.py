from __future__ import annotations

from typing import Any, Dict, List

from v2.accountability import apply_declared, apply_receipts
from v2.runtime_executor import execute_actions
from v2.validate import validate_named


class _Store:
    def __init__(self) -> None:
        self.awake = True
        self.woke = 0
        self.slept = 0

    def wake(self) -> None:
        self.awake = True
        self.woke += 1

    def sleep(self) -> None:
        self.awake = False
        self.slept += 1


class _App:
    def __init__(self) -> None:
        self.store = _Store()
        self._expecting_tasks = False
        self.web_q: List[str] = []
        self.open_t: List[Any] = []
        self.sp_cmd: List[Dict[str, Any]] = []

    def _handle_web_lookup(self, query: str) -> str:
        self.web_q.append(query)
        return "web ok"

    def _handle_open_link(self, target: Any) -> str:
        self.open_t.append(target)
        return "open ok"

    def _handle_spotify(self, meta: Dict[str, Any]) -> str:
        self.sp_cmd.append(meta)
        return "spotify ok"


def _fail(msg: str) -> None:
    raise SystemExit("FAIL: " + msg)


def main() -> None:
    request_id = "r1"
    pds: Dict[str, Any] = {}

    out = {
        "route_kind": "WEB_LOOKUP",
        "speak_text": "",
        "actions": [{"type": "WEB_LOOKUP_QUERY", "payload": {"query": "x"}}],
        "state_delta": {},
        "mode_set": "IDLE",
        "followup_until_utc": None,
        "debug": {},
    }

    ok, err = validate_named("EngineOutput", out)
    if not ok:
        _fail("validate EngineOutput failed: " + err)

    pds = apply_declared(pds, request_id, out)
    if "actions_declared" not in pds or not isinstance(pds["actions_declared"], list) or len(pds["actions_declared"]) != 1:
        _fail("actions_declared not recorded")

    app = _App()
    primary, receipts = execute_actions(app, request_id, out["actions"])
    if primary != "web ok":
        _fail("primary text mismatch")
    if not receipts or receipts[0].get("status") != "SUCCESS":
        _fail("receipt not success")
    if app.web_q != ["x"]:
        _fail("web handler not called")

    pds = apply_receipts(pds, receipts)
    if "actions_executed" not in pds or len(pds["actions_executed"]) != 1:
        _fail("actions_executed not recorded")
    if "outcomes" not in pds or len(pds["outcomes"]) != 1:
        _fail("outcomes not recorded")

    out2 = {
        "route_kind": "OPEN_LINK",
        "speak_text": "",
        "actions": [{"type": "OPEN_LINK_INDEX", "payload": {"target": "it"}}],
        "state_delta": {},
        "mode_set": "IDLE",
        "followup_until_utc": None,
        "debug": {},
    }

    ok2, err2 = validate_named("EngineOutput", out2)
    if not ok2:
        _fail("validate EngineOutput failed: " + err2)

    primary2, receipts2 = execute_actions(app, "r2", out2["actions"])
    if primary2 != "open ok":
        _fail("open primary mismatch")
    if app.open_t != ["it"]:
        _fail("open target not preserved")

    out3 = {
        "route_kind": "SPOTIFY",
        "speak_text": "",
        "actions": [{"type": "SPOTIFY_COMMAND", "payload": {"cmd": "pause"}}],
        "state_delta": {},
        "mode_set": "IDLE",
        "followup_until_utc": None,
        "debug": {},
    }

    ok3, err3 = validate_named("EngineOutput", out3)
    if not ok3:
        _fail("validate EngineOutput failed: " + err3)

    primary3, receipts3 = execute_actions(app, "r3", out3["actions"])
    if primary3 != "spotify ok":
        _fail("spotify primary mismatch")
    if not app.sp_cmd or app.sp_cmd[-1].get("cmd") != "pause":
        _fail("spotify cmd not called")

    out4 = {
        "route_kind": "WAKE",
        "speak_text": "",
        "actions": [{"type": "STATE_SET_AWAKE", "payload": {"awake": True}}],
        "state_delta": {},
        "mode_set": "IDLE",
        "followup_until_utc": None,
        "debug": {},
    }

    ok4, err4 = validate_named("EngineOutput", out4)
    if not ok4:
        _fail("validate EngineOutput failed: " + err4)

    _, _ = execute_actions(app, "r4", out4["actions"])
    if app.store.woke < 1:
        _fail("wake not executed")

    out5 = {
        "route_kind": "START_DAY",
        "speak_text": "",
        "actions": [{"type": "ENTER_TASK_INTAKE", "payload": {"enabled": True}}],
        "state_delta": {},
        "mode_set": "IDLE",
        "followup_until_utc": None,
        "debug": {},
    }

    ok5, err5 = validate_named("EngineOutput", out5)
    if not ok5:
        _fail("validate EngineOutput failed: " + err5)

    _, _ = execute_actions(app, "r5", out5["actions"])
    if not getattr(app, "_expecting_tasks", False):
        _fail("intake not enabled")

    print("ALL MONTH3 HANDSHAKE TESTS PASSED")


if __name__ == "__main__":
    main()
