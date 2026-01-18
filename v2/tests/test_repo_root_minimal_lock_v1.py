from pathlib import Path

def test_repo_root_is_minimal_commercial_only():
    """
    This repo is a procurement-safe governance reference artifact.
    Root must remain minimal so evaluators are not confused.

    Allowed at repo root:
    - README.md
    - .gitignore (optional)
    - v2/ (commercial artifact)
    - .github/ (CI only)
    - LICENSE / NOTICE (legal)
    """
    root = Path(".")
    allowed = {"README.md", ".gitignore", "v2", ".github", "LICENSE", "NOTICE"}
    ignore = {"venv", ".pytest_cache", "__pycache__"}

    found = []
    for p in root.iterdir():
        name = p.name
        if name == ".git":
            continue
        if name in ignore:
            continue
        found.append(name)

    unexpected = sorted([n for n in found if n not in allowed])
    assert not unexpected, f"Unexpected repo-root entries (commercial-only lock): {unexpected}"
