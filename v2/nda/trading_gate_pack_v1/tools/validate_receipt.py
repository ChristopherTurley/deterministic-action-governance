import json
import hashlib
import sys

CATEGORY_ORDER = {
  "STRUCTURAL": 0,
  "RISK": 1,
  "CAPS": 2,
  "MARKET_CONSTRAINT": 3,
  "PSYCHOLOGY": 4,
  "STATE_INTEGRITY": 5
}

def sha256_bytes(b):
  return hashlib.sha256(b).hexdigest()

def canonical_json_bytes(obj):
  return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")

def load_json(path):
  with open(path, "r", encoding="utf-8") as f:
    return json.load(f)

def code_category(code):
  if code.startswith("TH1_STRUCT_"):
    return "STRUCTURAL"
  if code.startswith("TH1_RISK_"):
    return "RISK"
  if code.startswith("TH1_CAP_"):
    return "CAPS"
  if code.startswith("TH1_MKT_"):
    return "MARKET_CONSTRAINT"
  if code.startswith("TH1_PSY_"):
    return "PSYCHOLOGY"
  if code.startswith("TH1_STATE_"):
    return "STATE_INTEGRITY"
  return "STATE_INTEGRITY"

def check_refusal_order(codes):
  last_cat = -1
  last_code = ""
  for c in codes:
    cat = code_category(c)
    cat_i = CATEGORY_ORDER.get(cat, 999)
    if cat_i < last_cat:
      raise ValueError("Refusal ordering violates category precedence")
    if cat_i == last_cat and c < last_code:
      raise ValueError("Refusal ordering violates lexicographic order within category")
    last_cat = cat_i
    last_code = c

def compute_receipt_hash(receipt):
  copy = dict(receipt)
  copy["receipt_hash"] = ""
  return sha256_bytes(canonical_json_bytes(copy))

def main():
  if len(sys.argv) != 4:
    raise SystemExit("usage: validate_receipt.py <receipt.json> <schema.json> <policy.json>")

  receipt_path = sys.argv[1]
  schema_path = sys.argv[2]
  policy_path = sys.argv[3]

  receipt = load_json(receipt_path)
  schema = load_json(schema_path)
  policy = load_json(policy_path)

  required = schema.get("required", [])
  for k in required:
    if k not in receipt:
      raise ValueError("Missing required field: " + k)

  if not isinstance(receipt.get("refusal_codes"), list):
    raise ValueError("refusal_codes must be an array")

  if receipt.get("refusal_count") != len(receipt.get("refusal_codes")):
    raise ValueError("refusal_count mismatch")

  allowed = set(policy.get("refusal_codes", []))
  for c in receipt.get("refusal_codes"):
    if c not in allowed:
      raise ValueError("Unknown refusal code: " + c)

  check_refusal_order(receipt.get("refusal_codes"))

  if receipt.get("ruleset_hash") != sha256_bytes(canonical_json_bytes(policy)):
    raise ValueError("ruleset_hash mismatch")

  if receipt.get("schema_hash") != sha256_bytes(canonical_json_bytes(schema)):
    raise ValueError("schema_hash mismatch")

  expected = compute_receipt_hash(receipt)
  if receipt.get("receipt_hash") != expected:
    raise ValueError("receipt_hash mismatch")

  return 0

if __name__ == "__main__":
  main()
