**Document Type:** Reference Library  
**Required for Evaluation:** No  
**Primary Evaluator Path:** `docs/START_HERE.md`

# Trading Hat v1 — Governance Specification (Canonical Hat Template)

Status: Draft v1 (Hat spec)
Scope: Governance-only
Power: Zero (restrictive + explanatory only)

## 1. Purpose
The Trading Hat applies domain-specific governance constraints to trading proposals to:
- make authority explicit
- enforce self-declared risk boundaries
- preserve discipline under pressure
- produce audit-ready decision records

Never:
- trade ideas, signals, recommendations
- broker/API execution
- monitoring, background behavior
- performance optimization

Execution remains external and host-owned.

## 2. Relationship to VERA Core
Does not modify core semantics.
Uses core: proposal → decision → explicit commit, refusal/failure taxonomy, ledger.
Commit records authority; it does not trigger execution.

## 3. Domain Declaration (Vocabulary Only)
Trade proposals:
- OPEN_TRADE
- ADD_POSITION
- REDUCE_POSITION
- CLOSE_POSITION
- ADJUST_RISK

Rule-boundary proposals:
- INCREASE_MAX_RISK
- OVERRIDE_RULE
- BREAK_DISCIPLINE_RULE

Meta:
- DECLARE_TRADING_RULES
- UPDATE_TRADING_RULES

## 4. Preconditions (Required Declarations)
Before evaluating trade proposals, trader must declare:
- max_loss_per_trade_usd
- max_daily_loss_usd
- max_trades_per_day
- allowed_instruments (e.g., shares, options, 0DTE)
- allowed_universe (tickers/asset classes)
- allowed_time_window
- explicit commit format (operator-defined)

Missing declarations → REFUSE (TTL_MISSING_CONTEXT or AUTH_AMBIGUOUS_INTENT).

## 5. Trading Invariants (Refusal-Only)
All violations → decision=REFUSE, category=INVARIANT.

Reason codes (stable, hat-scoped):
- INV_TRADING_MISSING_REQUIRED_FIELD
- INV_TRADING_MAX_LOSS_PER_TRADE_EXCEEDED
- INV_TRADING_MAX_DAILY_LOSS_EXCEEDED
- INV_TRADING_MAX_TRADES_PER_DAY_EXCEEDED
- INV_TRADING_INSTRUMENT_NOT_ALLOWED
- INV_TRADING_OUTSIDE_TIME_WINDOW
- INV_TRADING_OVERRIDE_REQUIRES_COMMIT

Notes:
- Overrides are allowed only as explicit commits; never inferred.
- No background monitoring; no delayed execution.

## 6. Refusal Semantics (Mapped, Not New Logic)
The Hat does not change refusal logic; it changes explanation language.
Examples:
- AUTH_NO_COMMIT → “This action requires an explicit trader commit.”
- AUTH_AMBIGUOUS_INTENT → “Missing trade details; cannot evaluate safely.”
- TTL_CONTEXT_EXPIRED → “Referenced context is expired; restate as a new proposal.”
- INV_TRADING_MAX_LOSS_PER_TRADE_EXCEEDED → “Proposed max loss exceeds your declared per-trade limit.”

## 7. Required Proposal Fields (Minimum)
For OPEN_TRADE / ADD_POSITION:
- instrument (shares/options)
- ticker
- direction (long/short)
- size (shares/contracts)
- max_loss_usd (explicit)

Missing fields → REFUSE (INV_TRADING_MISSING_REQUIRED_FIELD).

## 8. Decision Outcomes (Unchanged)
- REFUSE
- FAIL
- UNAVAILABLE
- ALLOW_FOR_COMMIT

ALLOW_FOR_COMMIT indicates eligibility for explicit authority only; it does not recommend execution.

## 9. Ledger Requirements
Every trade interaction records:
- proposal payload (immutable)
- decision + category + reason_code (if refusal)
- commit artifact (if any)
- timeline: proposal → decision → commit (optional) → outcome

No broker execution data required.

## 10. Post-hoc Explanation Artifacts (Read-only)
Allowed:
- drift summaries (e.g., repeated risk-limit refusals)
- TTL explanations
- timeline narratives

Never:
- coaching, nudging, advice

## 11. What This Hat Will Never Do
- signals, entries/exits, sizing recommendations
- broker automation or API execution
- background monitoring or alerts
- reuse prior approvals

## 12. Completion Criteria
Complete when:
- vocabulary is explicit
- invariants are refusal-only with stable reason codes
- commit/execution boundary is explicit
- removal does not affect core behavior
