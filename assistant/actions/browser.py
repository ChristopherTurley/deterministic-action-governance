from __future__ import annotations
import webbrowser

def open_url(url: str) -> bool:
    u = (url or "").strip()
    if not u:
        return False
    try:
        webbrowser.open(u, new=2)
        return True
    except Exception:
        return False
