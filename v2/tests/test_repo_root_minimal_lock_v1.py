from pathlib import Path

def test_repo_root_is_minimal_commercial_only():
    root = Path(".")
    allowed = {"README.md", ".gitignore", "v2", ".github", "LICENSE", "NOTICE"}
    ignore = {"venv", ".pytest_cache", "__pycache__", ".git"}

    found = []
    for pth in root.iterdir():
        name = pth.name
        if name in ignore:
            continue
        found.append(name)

    unexpected = sorted([n for n in found if n not in allowed])
    assert not unexpected, f"Unexpected repo-root entries (commercial-only lock): {unexpected}"
