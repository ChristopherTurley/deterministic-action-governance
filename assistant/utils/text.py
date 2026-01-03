from __future__ import annotations
import re

def normalize_text(t: str) -> str:
    t = (t or "").strip().lower()
    t = re.sub(r"\s+", " ", t)
    return t

def clean_text(text: str) -> str:
    t = normalize_text(text)
    t = re.sub(r"\b(please|thanks)\b", " ", t)
    t = re.sub(r"\s+", " ", t).strip(" ,.!?- ")
    return t.strip()
