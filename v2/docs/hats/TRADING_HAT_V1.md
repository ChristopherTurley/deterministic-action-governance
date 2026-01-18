# Trading Hat v1 (FROZEN)

STATUS
- Hat ID: TRADING_HAT_V1
- State: FROZEN
- Authority: NONE
- Execution: NONE
- Advisory: NONE

SCOPE (LOCKED)
Trading Hat v1 is a governance-only classifier that evaluates proposed trading intents against deterministic rules.
It does not recommend trades, size positions, access market data, or execute actions.
Refusal and inaction are correct outcomes.

INPUT CONTRACT (LOCKED)
Accepted fields only:
- instrument_type: equity | option | future | other
- strategy_class: defined_strategy | undefined_strategy
- risk_class: low | medium | high
- time_horizon: intraday | swing | long_term
- leverage_flag: true | false
- operator_declared_context: standard | experimental

Explicitly excluded:
- price, size, signal, probability, confidence

RULES (LOCKED, DETERMINISTIC ORDER)
- TRD-R-001: option + intraday + leverage_flag true -> REFUSE / EXCESSIVE_RISK_CLASS
- TRD-R-002: strategy_class undefined_strategy -> REFUSE / UNCLASSIFIED_STRATEGY
- TRD-R-003: operator_declared_context experimental -> NO-OP / CONTEXT_NOT_GOVERNABLE
- TRD-R-004: instrument_type other -> REFUSE / OUT_OF_SCOPE_INSTRUMENT
- TRD-R-005: equity + long_term + no leverage + defined_strategy + standard -> ALLOW / BASELINE_PERMITTED_CASE
- TRD-R-000: malformed input -> REFUSE / MALFORMED_INPUT

RECEIPT SCHEMA (LOCKED)
Fields:
- hat_id
- rule_id
- decision_type: ALLOW | REFUSE | NO-OP
- reason_code
- input_fingerprint (deterministic hash)
- decision_fingerprint (deterministic hash)
- logical_time_index (monotonic, non-wall-clock)

FREEZE STATEMENT
Trading Hat v1 is frozen. No rules, reason codes, schemas, or scenarios will be modified.
Future changes are Trading Hat v2 and are non-retroactive.


COMMIT (LOCKED)
Trading Hat v1 has ZERO execution authority. Any commit routed to this hat MUST fail-closed:
- decision_type: REFUSE
- reason_code: NO_EXECUTION
- rule_id: TRD-R-999
