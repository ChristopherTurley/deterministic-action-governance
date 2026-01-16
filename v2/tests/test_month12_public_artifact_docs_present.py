from pathlib import Path

DOCS = [
    "v2/docs/demo_index.md",
    "v2/docs/public/MONTH12_PUBLIC_ARTIFACT_LOCK.md",
    "v2/docs/public/APPLE_GAP_MAP_MONTH12.md",
    "v2/docs/public/ONE_PAGER.md",
    "v2/docs/public/INVESTOR_NARRATIVE.md",
    "v2/docs/public/DEMO_SCRIPT_VERBAL.md",
]

def test_month12_public_docs_exist() -> None:
    for rel in DOCS:
        p = Path(rel)
        assert p.exists(), f"missing: {rel}"
        s = p.read_text(encoding="utf-8", errors="strict").strip()
        assert len(s) > 0, f"empty: {rel}"
