import subprocess


def test_bridge_runner_unknown_hat_exits_nonzero():
    cmd = [
        "python3",
        "v2/bridge/run_hat_session.py",
        "--hat",
        "NOPE",
        "--context",
        "{}",
        "--proposal",
        "{}",
        "--commit",
        "{}",
    ]
    p = subprocess.run(cmd, capture_output=True, text=True)
    assert p.returncode != 0
