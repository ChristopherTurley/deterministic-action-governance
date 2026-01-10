from __future__ import annotations


# V2_WEB_MIRROR_HELPER: mirror v2 web results into the same channels v1 OPEN_LINK uses
def _v2_mirror_last_web(app, items):
    try:
        if hasattr(app, 'store') and hasattr(app.store, 'set_last_web'):
            app.store.set_last_web(items)
    except Exception:
        pass
    try:
        setattr(app, '_last_web_items', items)
    except Exception:
        pass
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
                # V2_WEB_ATTEMPT_MARKER: record last web attempt + mirror results for OPEN_LINK_INDEX truthfulness
                try:
                    setattr(app, "_last_web_attempted", True)
                except Exception:
                    pass
                q = str(payload.get("query", "") or "").strip()
                txt = app._handle_web_lookup(q)
                # V2_WEB_FORCE_EMPTY_MIRROR: ensure OPEN_LINK_INDEX can be truthful even when search returns 0 results
                try:
                    txt_str = txt if isinstance(txt, str) else ""
                    # If the handler said "No results found", explicitly record an empty result set.
                    if "No results found" in txt_str:
                        try:
                            setattr(app, "_last_web_items", [])
                        except Exception:
                            pass
                        try:
                            st = getattr(app, "store", None)
                            fn = getattr(st, "set_last_web", None) if st is not None else None
                            if callable(fn):
                                fn([])
                        except Exception:
                            pass
                    else:
                        # Otherwise, mirror whatever the app stored.
                        items2 = None
                        try:
                            st = getattr(app, "store", None)
                            fn = getattr(st, "get_last_web", None) if st is not None else None
                            if callable(fn):
                                items2 = fn()
                        except Exception:
                            items2 = None
                        if items2 is not None:
                            try:
                                setattr(app, "_last_web_items", items2)
                            except Exception:
                                pass
                except Exception:
                    pass
                if isinstance(txt, str) and txt:
                    primary_text = txt
                receipts.append(_receipt(request_id, at, payload, "SUCCESS", {"query": q}, None))
                continue

            if at == "OPEN_LINK_INDEX":
                # V2_OPEN_TRUTH_MARKER: if the last web search returned zero results, do not claim "search first"
                try:
                    attempted = bool(getattr(app, "_last_web_attempted", False))
                    items = getattr(app, "_last_web_items", None)
                    # V2_OPEN_TRUTH_STORE_FALLBACK: if _last_web_items is missing, consult store.get_last_web()
                    if items is None:
                        try:
                            st = getattr(app, "store", None)
                            fn = getattr(st, "get_last_web", None) if st is not None else None
                            if callable(fn):
                                items = fn()
                        except Exception:
                            pass
                    if attempted and isinstance(items, list) and len(items) == 0:
                        primary_text = "Your last web search returned no results, so there’s nothing to open. Try a different query."
                        receipts.append({"action_type": at, "status": "SUCCESS", "request_id": request_id, "payload": payload, "artifact": {"opened": False, "reason": "no_results"} , "error": None})
                        continue
                except Exception:
                    pass
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
