from pathlib import Path

BAD_PHRASES = [
    "sub-200ms",
    "latency guarantee",
    "AWS Marketplace",
    "Azure Marketplace",
    "plug-and-play",
    "middleware",
    "proxy",
    "dashboard",
    "toggle rules",
    "cryptographically signed",
    "tamper-proof log",
    "Docker image (a pre-packaged version) that includes",  # avoids selling runtime bundle as commercial artifact
]

SCAN_PATHS = [
    Path("README.md"),
    Path("v2/docs/public"),
    Path("v2/sales"),
]

def _iter_text_files(p: Path):
    if p.is_file():
        yield p
        return
    for f in p.rglob("*.md"):
        yield f

def test_no_procurement_claim_drift():
    texts = []
    for p in SCAN_PATHS:
        if not p.exists():
            continue
        for f in _iter_text_files(p):
            try:
                texts.append((f, f.read_text(encoding="utf-8", errors="ignore")))
            except Exception:
                continue

    found = []
    for f, txt in texts:
        low = txt.lower()
        for phrase in BAD_PHRASES:
            if phrase.lower() in low:
                found.append((str(f), phrase))
    assert not found, "forbidden_procurement_claims_present:\n" + "\n".join([f"{a}: {b}" for a,b in found])
