import subprocess
import sys
from pathlib import Path


def test_trading_hat_demo_invariants_are_stable():
    repo_root = Path(__file__).resolve().parents[2]
    script = repo_root / "v2" / "demo" / "trading_governance_demo.py"

    env = dict(**{"PYTHONPATH": str(repo_root)})
    out = subprocess.check_output([sys.executable, str(script)], cwd=str(repo_root), env=env, text=True)

    # Load-bearing invariants only (no full golden snapshot).
    assert "SCENARIO A — ALLOWED (PROPOSE + COMMIT)" in out
    assert out.count("decision: ALLOW") >= 2

    assert "SCENARIO B — REFUSED (RISK LIMIT)" in out
    assert "decision: REFUSE" in out
    assert "risk_daily_loss_limit_reached_or_exceeded" in out

    assert "SCENARIO C — REQUIRE RE-COMMIT (COMMIT DRIFT)" in out
    assert "decision: REQUIRE_RECOMMIT" in out
    assert "proposal_drift_requires_recommit:size" in out
