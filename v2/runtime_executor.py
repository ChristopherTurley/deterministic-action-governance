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

            if at == "TIME_READ":
                # Read-only: receipt required, no side effects beyond returning time info
                iso = ""
                tz = ""
                try:
                    # Prefer app-provided time if available
                    fn = getattr(app, "_handle_time", None)
                    if callable(fn):
                        out = fn()
                        if isinstance(out, dict):
                            iso = str(out.get("iso", "") or "")
                            tz = str(out.get("tz", "") or "")
                    if not iso:
                        from datetime import datetime, timezone
                        iso = datetime.now(timezone.utc).isoformat()
                        tz = "UTC"
                except Exception:
                    from datetime import datetime, timezone
                    iso = datetime.now(timezone.utc).isoformat()
                    tz = "UTC"
                receipts.append(_receipt(request_id, at, payload, "SUCCESS", {"iso": iso, "tz": tz}, None))
                continue

            if at == "PRIORITY_GET":
                # Read-only: receipt required
                items = None
                try:
                    fn = getattr(app, "_handle_priority_get", None)
                    if callable(fn):
                        items = fn()
                except Exception:
                    items = None
                meta = {"count": len(items) if isinstance(items, list) else 0}
                receipts.append(_receipt(request_id, at, payload, "SUCCESS", meta, None))
                continue

            if at == "PRIORITY_SET":
                # State change: still must be receipted (actual state mutation occurs inside app handler)
                item = payload.get("item", None)
                pr = payload.get("priority", None)
                ok = True
                try:
                    fn = getattr(app, "_handle_priority_set", None)
                    if callable(fn):
                        fn(item, pr)
                except Exception as e:
                    ok = False
                    receipts.append(_receipt(request_id, at, payload, "FAILURE", {"item": item, "priority": pr}, repr(e)))
                    continue
                receipts.append(_receipt(request_id, at, payload, "SUCCESS", {"item": item, "priority": pr, "ok": ok}, None))
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
