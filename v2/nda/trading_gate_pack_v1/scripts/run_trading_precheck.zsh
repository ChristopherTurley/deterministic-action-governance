#!/usr/bin/env zsh
set -e
RECEIPT_PATH="$1"
python3 tools/validate_receipt.py "$RECEIPT_PATH" schema/trading_hat_receipt_schema_v1.json policy/trading_hat_rules_v1.json
