import re
from pathlib import Path
from typing import Set

import v2.coat.templates_v1 as templates_v1


RE_REASON = re.compile(r"\bINV_[A-Z0-9_]+\b")


def _registry_reason_codes() -> Set[str]:
    p = Path("v2/docs/hats/HAT_REASON_CODES_REGISTRY_V1.md")
    assert p.exists(), "Missing canonical reason code registry: docs/hats/hat_reason_codes_registry_v1.md"
    text = p.read_text(encoding="utf-8", errors="strict")
    return set(RE_REASON.findall(text))


def _template_keys() -> Set[str]:
    keys: Set[str] = set()
    for _, val in vars(templates_v1).items():
        if isinstance(val, dict):
            for k in val.keys():
                if isinstance(k, str):
                    keys.add(k)
    return keys


def test_coat_templates_cover_reason_code_registry():
    registry = _registry_reason_codes()
    assert registry, "No INV_* codes found in registry; registry format unexpected."

    tmpl = _template_keys()
    assert tmpl, "No template keys found in v2/coat/templates_v1.py"

    missing = sorted([c for c in registry if (not c.endswith("_")) and c not in tmpl])

    assert not missing, "Missing coat templates for registry reason codes: " + ", ".join(missing)
