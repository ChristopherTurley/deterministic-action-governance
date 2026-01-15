# HOSTILE REVIEW (MISUSE + DRIFT HARDENING)

This document answers the questions a skeptical reviewer will ask.
It adds no capability. It only reduces ambiguity.

## Canonical Claims (must remain true)
- This repo is a reference artifact, not a product.
- No externally meaningful action occurs without explicit, attributable human authority.
- Deterministic, fail-closed behavior is the default.
- Refusal and inaction are correct outcomes.
- Hats never execute and never escalate authority.
- Coats only explain; removing a coat never changes execution.

## Attack Surface Inventory (what a reviewer will probe)
1) Entrypoints:
   - Question: "Where does execution begin and can it vary pre-governance?"
   - Required property: entrypoints are sterile airlocks (no flags, no env branching, no intelligence).

2) Background execution:
   - Question: "Is there any scheduler, retry loop, async task, daemon, or timer?"
   - Required property: none. No background execution, no retries, no escalation.

3) Side effects:
   - Question: "Do any modules perform side effects directly (network, subprocess, filesystem writes beyond logs)?"
   - Required property: default-deny side effects; explicit commit required; attributable authority recorded.

4) Day-side hat drift:
   - Question: "Does any hat advise, recommend, optimize, or instruct action?"
   - Required property: day-side may explain/simulate/reflect only; no advice or optimization language.

5) Demo ambiguity:
   - Question: "Do demos imply capability beyond refusal-governed execution?"
   - Required property: demos showcase refusal and restraint; demos are non-authoritative.

6) Deposit ambiguity:
   - Question: "Is there staging of future product behavior?"
   - Required property: deposits are non-canonical reference material only; not an execution surface.

## How to Verify (read-only checks)
Run these from repo root:

A) Entrypoint discretion (args/env branching) should be absent:
- search for argparse, sys.argv, click/typer, os.environ in entrypoints/runtime.

B) Background execution primitives should be absent:
- search for threading/async scheduling/timers/retry/backoff/while-true/sleep.

C) Side-effect primitives should be tightly controlled or absent:
- search for subprocess/os.system/network clients.

D) Hat language must not contain advice/optimization:
- search docs for "recommend", "you should", "best", "optimal", "buy/sell/entry/exit".

If any check produces results, interpretation must be fail-closed:
- if it implies autonomy or discretion -> reject or remove
- if it is doc-only ambiguity -> clarify language (no new promises)

