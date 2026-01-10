# V2 Side-Effects Contract v1 (Month 8)

## Purpose
Side effects are never implicit. VERA may describe and prepare actions, but execution is governed by explicit policy.

## Core Rules (Tested Gates)
- Default policy is deny all.
- Allow-list permits only explicitly listed action kinds.
- Even when allowed, Month 8 does not perform real side effects; it returns deterministic receipts.
- Every executor receipt contains reversibility metadata:
  - reversal_id
  - undo_hint

## Receipt Types
- ACTION_BLOCKED_POLICY
  - blocked_reason = default_safe
- ACTION_DRY_RUN

## Policy Surface
- v2/side_effect_policy.py
  - DEFAULT_POLICY.allowed_actions = []
  - is_action_allowed(kind, policy)

## Determinism
Same input actions + same policy => same receipts.
