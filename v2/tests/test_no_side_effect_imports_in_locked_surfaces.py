from pathlib import Path

BANNED = [
    "subprocess",
    "requests",
    "webbrowser",
    "urllib.request",
    "socket",
]

# Keep this intentionally conservative: only scan "locked surfaces" paths.
TARGETS = [
    "v2/hats/router_v1.py",
    "v2/coat/coat_v1.py",
]

def test_no_obvious_side_effect_imports_in_locked_surfaces() -> None:
    for rel in TARGETS:
        p = Path(rel)
        s = p.read_text(encoding="utf-8", errors="strict")
        for b in BANNED:
            assert f"import {b}" not in s
            assert f"from {b} import" not in s
