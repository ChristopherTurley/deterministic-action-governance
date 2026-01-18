from __future__ import annotations

from pathlib import Path

CORE_PATHS = ['v2/hats/hat_interface.py', 'v2/hats/router_v1.py', 'v2/hats/registry.py', 'v2/hats/reason_allowlists_v1.py', 'v2/coat/coat_v1.py', 'v2/coat/templates_v1.py', 'v2/device_b/MANIFEST.json', 'v2/device_b/generate_manifest.py', 'v2/device_b/verify_all.py', 'v2/docs/public/COMMERCIAL_BUNDLE_V1.md', 'v2/docs/public/CORE_SURFACE_V1.md']

FORBIDDEN_IMPORT_TOKENS = [
    "assistant.",         # legacy runtime tree
    "spotipy", "requests", "selenium", "playwright",
    "tavily", "serpapi", "duckduckgo",
]

def test_core_surface_paths_exist():
    missing = [p for p in CORE_PATHS if not Path(p).exists()]
    assert not missing, f"Missing core surface paths: {missing}"

def test_core_surface_has_no_legacy_runtime_imports():
    offenders = []
    for p in CORE_PATHS:
        pp = Path(p)
        if not pp.exists() or pp.is_dir():
            continue
        txt = pp.read_text(encoding="utf-8", errors="ignore")
        for tok in FORBIDDEN_IMPORT_TOKENS:
            if tok in txt:
                offenders.append((p, tok))
    assert not offenders, f"Core surface contains forbidden import tokens: {offenders}"
