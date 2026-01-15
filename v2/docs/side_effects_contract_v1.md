# V2 Side-Effects Contract v1

This document defines the non-negotiable contract for side-effects in VERA v2.
It exists to guarantee:
- deterministic behavior
- fail-closed execution
- explicit operator commit gates
- audit-safe reversibility metadata

## Core Rules

1) **Default deny**
- If an action is not explicitly allowed by policy, it MUST be blocked.
- Blocking MUST return a receipt of type `ACTION_BLOCKED_POLICY`.

2) **No real-world execution from v2 demos/tests**
- Any demo or test path must be safe by default.
- When running in dry-run mode, receipts MUST be `ACTION_DRY_RUN`.

3) **Every blocked or simulated action is reversible (metadata)**
- Every `ACTION_BLOCKED_POLICY` and `ACTION_DRY_RUN` receipt MUST include:
  - `reversal_id` (stable identifier used to correlate a potential undo)
  - `undo_hint` (human-readable instruction for undoing or dismissing)

4) **Operator commit required**
- Proposals are non-binding.
- Side-effects require explicit operator commit (outside the engine).

## Receipt Types

### ACTION_BLOCKED_POLICY
Used when an action is denied by policy (default-safe, allowlist missing, conflicts, etc.)

Minimum fields:
- `type`: `ACTION_BLOCKED_POLICY`
- `blocked_reason`: policy reason code (e.g., `default_safe`)
- `reversal_id`: unique id string
- `undo_hint`: short human instruction

### ACTION_DRY_RUN
Used when an action is simulated (never executed), including demo and test runs.

Minimum fields:
- `type`: `ACTION_DRY_RUN`
- `simulated_reason`: reason code
- `reversal_id`: unique id string
- `undo_hint`: short human instruction

## Notes

- These rules are intentionally strict.
- The engine must never “do the thing” silently.
- The only permitted outcomes are deterministic receipts with audit metadata.
