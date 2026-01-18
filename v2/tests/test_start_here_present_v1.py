from pathlib import Path

def test_start_here_script_present_and_points_to_commercial_artifact():
    p = Path("v2/tools/start_here.sh")
    assert p.exists(), "Missing evaluator entrypoint: v2/tools/start_here.sh"
    txt = p.read_text(encoding="utf-8", errors="ignore")
    assert "run_commercial_suite_v1.sh" in txt
    assert "v2.device_b.verify_all" in txt
    assert "REPO_MAP_COMMERCIAL_V1.md" in txt
