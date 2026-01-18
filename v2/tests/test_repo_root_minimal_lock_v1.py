from pathlib import Path

def test_repo_root_is_minimal_commercial_only():
    """
    Procurement-safe governance reference artifact.
    Root must remain minimal so evaluators are not confused.

    Allowed at repo root:
    - README.md
    - .gitignore (optional)
    - v2/ (commercial artifact)
    - .github/ (CI only)
    - LICENSE / NOTICE (procurement expects these)

    Local-only entries are ignored:
    - venv
    - .pytest_cache
    - __pycache__
    """
    root = Path(".")
    allowed = {"README.md", ".gitignore", "v2", ".github", "LICENSE", "NOTICE"}
    ignore = {"venv", ".pytest_cache", "__pycache__"}

    forbid_paths = [
        "legacy_root",
        "v2/legacy_root",
    ]
    for fp in forbid_paths:
        assert not Path(fp).exists(), f"Forbidden path present: {fp}"

    found = []
    for pth in root.iterdir():
        name = pth.name
        if name == ".git":
            continue
        if name in ignore:
            continue
        found.append(name)

    unexpected = sorted([n for n in found if n not in allowed])
    assert not unexpected, f"Unexpected repo-root entries (commercial-only lock): {unexpected}"
