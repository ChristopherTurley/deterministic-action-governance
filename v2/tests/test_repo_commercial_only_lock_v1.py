from __future__ import annotations

import subprocess


def _tracked() -> list[str]:
    return subprocess.check_output(["git", "ls-files"], text=True).splitlines()


def test_repo_is_commercial_bundle_only_no_legacy_runtime_surfaces():
    files = _tracked()

    forbidden_prefixes = [
        "assistant/",
        "docs/",
        "demo/",
        "spec/",
        "vera_v2_public_deposit/",
    ]

    forbidden_exact = [
        "run_vera.py",
        "run_vera_v2.py",
        "demo_trading_hat_v1.sh",
        "EVALUATE.md",
        "GLOSSARY.md",
        "SECURITY.md",  # allowed at root only; this exact check is safe because we keep it
    ]

    # NOTE: SECURITY.md is allowed; remove it from forbidden_exact if present.
    forbidden_exact = [x for x in forbidden_exact if x != "SECURITY.md"]

    bad = []
    for f in files:
        if any(f.startswith(pref) for pref in forbidden_prefixes):
            bad.append(f)
            continue
        if f in forbidden_exact:
            bad.append(f)

        # Keep .github clean: only workflows allowed
        if f.startswith(".github/") and not f.startswith(".github/workflows/"):
            bad.append(f)

    assert not bad, "repo_contains_out_of_scope_files:\n" + "\n".join(sorted(set(bad)))
