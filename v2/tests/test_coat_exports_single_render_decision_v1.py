from pathlib import Path

def test_coat_has_single_render_decision_v1_definition() -> None:
    s = Path("v2/coat/coat_v1.py").read_text(encoding="utf-8", errors="strict")
    assert s.count("def render_decision_v1") == 1
