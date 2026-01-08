import json

path = "v2/schema.json"
with open(path, "r", encoding="utf-8") as f:
    s = json.load(f)

defs = s.get("$defs")
if not isinstance(defs, dict) or not defs:
    raise SystemExit("schema_missing_or_empty_defs")

pds = defs.get("PersistentDailyState")
if not isinstance(pds, dict):
    raise SystemExit("schema_missing_pds")

if not isinstance(pds.get("properties"), dict):
    pds["properties"] = {}

pds_props = pds["properties"]

defs.setdefault("CommitmentState", {"type": "string", "enum": ["ACTIVE", "DONE", "CARRIED", "DROPPED"]})

defs.setdefault("DecayModel", {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "type": {"type": "string", "enum": ["NONE", "LINEAR", "STEP"]},
        "half_life_hours": {"type": "number", "minimum": 0, "default": 0}
    },
    "required": ["type", "half_life_hours"],
})

defs.setdefault("Commitment", {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "id": {"type": "string", "minLength": 1},
        "title": {"type": "string", "minLength": 1},
        "due_local_date": {"anyOf": [{"$ref": "#/$defs/ISODate"}, {"type": "null"}], "default": None},
        "importance": {"type": "integer", "minimum": 1, "maximum": 5, "default": 3},
        "decay": {"$ref": "#/$defs/DecayModel"},
        "state": {"$ref": "#/$defs/CommitmentState"},
        "depends_on": {"type": "array", "items": {"type": "string"}, "default": []},
        "notes": {"type": "string", "default": ""}
    },
    "required": ["id", "title", "due_local_date", "importance", "decay", "state", "depends_on", "notes"],
})

defs.setdefault("Dependency", {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "a": {"type": "string", "minLength": 1},
        "b": {"type": "string", "minLength": 1},
        "kind": {"type": "string", "enum": ["SOFT", "HARD"], "default": "SOFT"}
    },
    "required": ["a", "b", "kind"],
})

defs.setdefault("Blocker", {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "id": {"type": "string", "minLength": 1},
        "title": {"type": "string", "minLength": 1},
        "severity": {"type": "integer", "minimum": 1, "maximum": 5, "default": 3},
        "owner": {"type": "string", "default": ""},
        "notes": {"type": "string", "default": ""}
    },
    "required": ["id", "title", "severity", "owner", "notes"],
})

defs.setdefault("Momentum", {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "score": {"type": "integer", "minimum": 0, "maximum": 100, "default": 50},
        "reasons": {"type": "array", "items": {"type": "string"}, "default": []},
        "updated_utc": {"anyOf": [{"$ref": "#/$defs/ISODateTime"}, {"type": "null"}], "default": None}
    },
    "required": ["score", "reasons", "updated_utc"],
})

pds_props.setdefault("commitments", {"type": "array", "items": {"$ref": "#/$defs/Commitment"}, "default": []})
pds_props.setdefault("dependencies", {"type": "array", "items": {"$ref": "#/$defs/Dependency"}, "default": []})
pds_props.setdefault("blockers", {"type": "array", "items": {"$ref": "#/$defs/Blocker"}, "default": []})
pds_props.setdefault("momentum", {"$ref": "#/$defs/Momentum"})

with open(path, "w", encoding="utf-8") as f:
    json.dump(s, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("patched_ok")
