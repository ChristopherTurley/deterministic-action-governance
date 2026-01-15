from __future__ import annotations

# Canonical reducer entry point for tests and future wiring.
# This file exists to avoid guessing import paths across refactors.

from typing import Any

def reduce_state(state: Any, receipt_or_rr: Any) -> Any:
    # Try the known candidates in order. Keep this list tiny and explicit.
    last_err = None
    for mod, fn in [
        ("v2.state_reducer", "reduce_state"),
        ("v2.core.state_reducer", "reduce_state"),
        ("v2.reducer", "reduce_state"),
    ]:
        try:
            m = __import__(mod, fromlist=[fn])
            f = getattr(m, fn)
            return f(state, receipt_or_rr)
        except Exception as e:
            last_err = e
    raise ImportError(f"reduce_state not importable from known locations; last error: {last_err!r}")
