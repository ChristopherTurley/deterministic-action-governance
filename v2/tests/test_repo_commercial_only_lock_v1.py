from __future__ import annotations

from pathlib import Path


def _all_files_relposix(root: Path) -> list[str]:
    ignore_dirs = {".git", "venv", ".pytest_cache", "__pycache__"}
    out: list[str] = []
    for p in root.rglob("*"):
        if p.is_dir():
            continue
        parts = set(p.parts)
        if parts & ignore_dirs:
            continue
        out.append(p.relative_to(root).as_posix())
    return out


def test_repo_is_commercial_bundle_only_no_legacy_runtime_surfaces():
    root = Path(".").resolve()
    files = _all_files_relposix(root)

    # These are forbidden surfaces that would revive rebuttal risk.
    forbidden_prefixes = (
        "assistant/",
        "artifacts/",
        "legacy_root/",
        "v2/legacy_root/",
    )

    # Forbid runtime *surfaces* by path segment, not substring in filenames.
    forbidden_segments = (
        "/runtime/",
        "runtime/",  # also catches leading segment "runtime/..."
        "v2/runtime/",
    )

    for f in files:
        for pref in forbidden_prefixes:
            assert not f.startswith(pref), f"Forbidden path present: {f}"

        for seg in forbidden_segments:
            assert seg not in f, f"Forbidden runtime surface segment '{seg}' in file path: {f}"
