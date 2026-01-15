import re

import v2.coat.templates_v1 as templates_v1


BANNED_PATTERNS = [
    r"\byou should\b",
    r"\btry\b",
    r"\bconsider\b",
    r"\brecommend\b",
    r"\bsuggest\b",
    r"\bnext time\b",
    r"\byou may want\b",
    r"\bif you\b",
]


def _iter_template_strings():
    for _, val in vars(templates_v1).items():
        if isinstance(val, dict):
            for _, tmpl in val.items():
                if isinstance(tmpl, str):
                    yield tmpl


def test_coat_templates_contain_no_advice_language():
    texts = list(_iter_template_strings())
    assert texts, "No template strings found; templates surface missing or unexpected."

    banned = [re.compile(pat, flags=re.IGNORECASE) for pat in BANNED_PATTERNS]

    violations = []
    for t in texts:
        for rx in banned:
            if rx.search(t):
                violations.append((rx.pattern, t))
                break

    assert not violations, "Coat templates contain advice-like language: " + "; ".join(
        [f"{pat} -> {txt}" for pat, txt in violations[:5]]
    )
