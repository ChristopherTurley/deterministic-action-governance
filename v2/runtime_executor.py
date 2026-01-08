from __future__ import annotations

import time
from typing import Any, Dict, List, Optional, Tuple


def _utc_now_str() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _receipt(
    request_id: str,
    action_type: str,
    payload: Dict[str, Any],
    status: str,
    artifact: Optional[Dict[str, Any]] = None,
    error: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "request_id": request_id,
        "action_type": action_type,
        "payload": payload if isinstance(payload, dict) else {},
        "status": status,
        "executed_at_utc": _utc_now_str(),
        "artifact": artifact,
        "error": error,
    }


def execute_actions(app: Any, request_id: str, actions: List[Dict[str, Any]]) -> Tuple[str, List[Dict[str, Any]]]:
    primary_text = ""
    receipts: List[Dict[str, Any]] = []

    for a in actions or []:
        if not isinstance(a, dict):
            continue
        at = str(a.get("type", "") or "")
        payload = a.get("payload", {})
        if not isinstance(payload, dict):
            payload = {}

        try:
            if at == "STATE_SET_AWAKE":
                awake = bool(payload.get("awake", True))
                if awake:
                    app.store.wake()
                else:
                    app.store.sleep()
                receipts.append(_receipt(request_id, at, payload, "SUCCESS", {"awake": awake}, None))
                continue

            if at == "ENTER_TASK_INTAKE":
                enabled = bool(payload.get("enabled", True))
                try:
                    setattr(app, "_expecting_tasks", enabled)
                except Exception:
                    pass
                receipts.append(_receipt(request_id, at, payload, "SUCCESS", {"enabled": enabled}, None))
                continue

            if at == "WEB_LOOKUP_QUERY":
                q = str(payload.get("query", "") or "").strip()
                txt = app._handle_web_lookup(q)
                if isinstance(txt, str) and txt:
                    primary_text = txt
                receipts.append(_receipt(request_id, at, payload, "SUCCESS", {"query": q}, None))
                continue

            if at == "OPEN_LINK_INDEX":
                target = payload.get("target", None)
                txt = app._handle_open_link(target)
                if isinstance(txt, str) and txt:
                    primary_text = txt
                receipts.append(_receipt(request_id, at, payload, "SUCCESS", {"target": target}, None))
                continue

            if at == "SPOTIFY_COMMAND":
                cmd = str(payload.get("cmd", "") or "")
                query = payload.get("query", None)
                meta = {"cmd": cmd}
                if query is not None:
                    meta["query"] = str(query)
                txt = app._handle_spotify(meta)
                if isinstance(txt, str) and txt:
                    primary_text = txt
                receipts.append(_receipt(request_id, at, payload, "SUCCESS", {"cmd": cmd, "query": query}, None))
                continue

            receipts.append(_receipt(request_id, at, payload, "SKIPPED", None, "unknown action"))
        except Exception as e:
            receipts.append(_receipt(request_id, at, payload, "FAILURE", None, repr(e)))

    return primary_text, receipts
