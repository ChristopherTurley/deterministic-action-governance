from __future__ import annotations

import json
from pathlib import Path

from v2.hats.trading_hat_v1 import evaluate, schema_contract


def test_receipt_schema_is_locked():
    c = schema_contract()
    assert c["hat_id"] == "TRADING_HAT_V1"
    assert c["decision_type_enum"] == ["ALLOW", "REFUSE", "NO-OP"]
    assert "receipt_fields" in c
    assert c["receipt_fields"] == [
        "hat_id",
        "rule_id",
        "decision_type",
        "reason_code",
        "input_fingerprint",
        "decision_fingerprint",
        "logical_time_index",
    ]


def test_canonical_scenarios_match_expected_decisions():
    p = Path("v2/reference/trading_hat_v1/scenarios.json")
    data = json.loads(p.read_text(encoding="utf-8"))
    for s in data["scenarios"]:
        r = evaluate(s["input"], int(s["logical_time_index"]))
        expect = s["expect"]
        assert r["hat_id"] == "TRADING_HAT_V1"
        assert r["decision_type"] == expect["decision_type"]
        assert r["reason_code"] == expect["reason_code"]
        assert r["rule_id"] == expect["rule_id"]
        for k in [
            "input_fingerprint",
            "decision_fingerprint",
        ]:
            assert isinstance(r[k], str)
            assert len(r[k]) == 64
        assert isinstance(r["logical_time_index"], int)


def test_determinism_same_input_same_output():
    payload = {
        "instrument_type": "equity",
        "strategy_class": "defined_strategy",
        "risk_class": "low",
        "time_horizon": "long_term",
        "leverage_flag": False,
        "operator_declared_context": "standard",
    }
    r1 = evaluate(payload, 7)
    r2 = evaluate(payload, 7)
    assert r1 == r2
