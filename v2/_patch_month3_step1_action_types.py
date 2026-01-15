from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parent
SCHEMA = ROOT / "schema.json"
ENGINE_ADAPTER = ROOT / "engine_adapter.py"
RUNTIME_EXECUTOR = ROOT / "runtime_executor.py"

# New required action types introduced by Month 3 Step (1)
NEW_TYPES = [
    "TIME_READ",
    "PRIORITY_GET",
    "PRIORITY_SET",
    "ENTER_TASK_INTAKE",
    "STATE_SET_AWAKE",
]

# Anchor types already known to exist in your system (used to find the correct enum / allowlist block)
ANCHOR_TYPES = [
    "WEB_LOOKUP_QUERY",
    "OPEN_LINK_INDEX",
    "SPOTIFY_COMMAND",
]


def _load_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _save_json(p: Path, obj: Any) -> None:
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _walk(obj: Any, path: str = "") -> List[Tuple[str, Any]]:
    out: List[Tuple[str, Any]] = []
    if isinstance(obj, dict):
        out.append((path, obj))
        for k, v in obj.items():
            out.extend(_walk(v, f"{path}.{k}" if path else k))
    elif isinstance(obj, list):
        out.append((path, obj))
        for i, v in enumerate(obj):
            out.extend(_walk(v, f"{path}[{i}]"))
    return out


def patch_schema_action_type_enum() -> bool:
    data = _load_json(SCHEMA)
    candidates: List[Tuple[str, Dict[str, Any]]] = []

    for pth, node in _walk(data):
        if isinstance(node, dict) and "enum" in node and isinstance(node["enum"], list):
            enum_list = node["enum"]
            if not all(isinstance(x, str) for x in enum_list):
                continue
            # Find the "action type" enum by anchors already in your system
            hits = sum(1 for a in ANCHOR_TYPES if a in enum_list)
            if hits >= 2:
                candidates.append((pth, node))

    if not candidates:
        print("[SCHEMA] ERROR: Could not locate action type enum containing anchors:", ANCHOR_TYPES)
        return False

    # Choose the most likely: the one with the largest enum list
    candidates.sort(key=lambda t: len(t[1]["enum"]), reverse=True)
    chosen_path, chosen_node = candidates[0]

    enum_list = chosen_node["enum"]
    before = set(enum_list)
    changed = False
    for t in NEW_TYPES:
        if t not in before:
            enum_list.append(t)
            changed = True

    if changed:
        chosen_node["enum"] = sorted(set(enum_list))
        _save_json(SCHEMA, data)
        print(f"[SCHEMA] Patched action type enum at: {chosen_path}")
        print("[SCHEMA] Added:", ", ".join([t for t in NEW_TYPES if t not in before]))
    else:
        print(f"[SCHEMA] No change needed (all new types already present) at: {chosen_path}")

    return True


def patch_engine_adapter_allowlist() -> bool:
    txt = ENGINE_ADAPTER.read_text(encoding="utf-8")

    # Locate a likely allowlist block by finding a set/list literal that contains anchors
    # This is intentionally conservative: we only patch when we can find a contiguous block
    # that includes at least 2 anchor types.
    anchor_regex = r"(" + "|".join(re.escape(a) for a in ANCHOR_TYPES) + r")"
    anchor_hits = len(re.findall(anchor_regex, txt))
    if anchor_hits < 2:
        print("[ADAPTER] ERROR: Could not find enough anchor action types in engine_adapter.py to patch allowlist safely.")
        return False

    # Patch strategy:
    # Find the first occurrence of a block like {...} or [...] that contains at least 2 anchors.
    # Then insert any missing NEW_TYPES as string literals before the closing brace/bracket.
    pattern = re.compile(
        r"(?P<prefix>\b[A-Z0-9_]*ALLOWLIST\b\s*=\s*)(?P<block>\{.*?\}|\[.*?\])",
        re.DOTALL,
    )

    m = pattern.search(txt)
    if not m:
        # Some repos name it differently; try any uppercase constant assignment containing anchors
        pattern2 = re.compile(r"(?P<prefix>\b[A-Z0-9_]+\b\s*=\s*)(?P<block>\{.*?\}|\[.*?\])", re.DOTALL)
        for mm in pattern2.finditer(txt):
            block = mm.group("block")
            hits = sum(1 for a in ANCHOR_TYPES if a in block)
            if hits >= 2:
                m = mm
                break

    if not m:
        print("[ADAPTER] ERROR: Could not locate an allowlist-like block to patch safely.")
        return False

    block = m.group("block")
    hits = sum(1 for a in ANCHOR_TYPES if a in block)
    if hits < 2:
        print("[ADAPTER] ERROR: Matched a block, but it did not contain enough anchors. Refusing to patch.")
        return False

    missing = [t for t in NEW_TYPES if f'"{t}"' not in block and f"'{t}'" not in block]
    if not missing:
        print("[ADAPTER] No change needed (all new types already in allowlist block).")
        return True

    # Insert with same quote style as existing anchors if possible
    quote = "'" if ("'WEB_LOOKUP_QUERY'" in block or "'OPEN_LINK_INDEX'" in block or "'SPOTIFY_COMMAND'" in block) else '"'
    insertion = "".join([f"    {quote}{t}{quote},\n" for t in missing])

    if block.startswith("{"):
        new_block = re.sub(r"\}\s*$", insertion + "}", block, flags=re.DOTALL)
    else:
        new_block = re.sub(r"\]\s*$", insertion + "]", block, flags=re.DOTALL)

    new_txt = txt[: m.start("block")] + new_block + txt[m.end("block") :]

    ENGINE_ADAPTER.write_text(new_txt, encoding="utf-8")
    print("[ADAPTER] Patched allowlist-like block in engine_adapter.py")
    print("[ADAPTER] Added:", ", ".join(missing))
    return True


def patch_runtime_executor_receipts() -> bool:
    txt = RUNTIME_EXECUTOR.read_text(encoding="utf-8")

    # We do not refactor. We only patch if there is an obvious dispatch table/dict keyed by action type.
    # Common patterns:
    # - HANDLERS = {"WEB_LOOKUP_QUERY": fn, ...}
    # - if action["type"] == "...": ...
    #
    # If we can't find a safe insertion point, we won't edit this file.
    added_any = False

    # Pattern A: HANDLERS dict
    handlers_pat = re.compile(r"(?P<name>\b[A-Z0-9_]*HANDLERS\b)\s*=\s*\{(?P<body>.*?)\n\}", re.DOTALL)
    hm = handlers_pat.search(txt)
    if hm:
        body = hm.group("body")
        missing = [t for t in NEW_TYPES if t not in body]
        if missing:
            # Insert minimal receipt-only handler references; we assume a generic receipt helper exists.
            # If not, this will be caught by tests/compile and we will patch explicitly next.
            insert_lines = []
            for t in missing:
                insert_lines.append(f'  "{t}": _handle_receipt_only,\n')
            new_body = body + "\n" + "".join(insert_lines)
            new_txt = txt[: hm.start("body")] + new_body + txt[hm.end("body") :]
            RUNTIME_EXECUTOR.write_text(new_txt, encoding="utf-8")
            print("[EXECUTOR] Added new types to HANDLERS dict (expects _handle_receipt_only).")
            print("[EXECUTOR] Added:", ", ".join(missing))
            return True

    # Pattern B: if/elif chain on action type — add explicit branches returning receipts
    if_pat = re.compile(r'if\s+.*?get\(["\']type["\']\).*?:', re.DOTALL)
    if not if_pat.search(txt):
        print("[EXECUTOR] No safe dispatch pattern found (HANDLERS dict or if/elif chain). Leaving runtime_executor.py unchanged.")
        return True

    # If there is an if/elif chain, we still refuse to patch blindly without seeing a stable anchor.
    # We just confirm anchors exist and tell you the exact next step if needed.
    anchor_hits = sum(1 for a in ANCHOR_TYPES if a in txt)
    if anchor_hits < 2:
        print("[EXECUTOR] Found a type-dispatch pattern, but not enough anchors to patch safely. Leaving runtime_executor.py unchanged.")
        return True

    print("[EXECUTOR] Detected type-dispatch pattern but did not auto-edit (conservative).")
    print("[EXECUTOR] If TIME_READ/PRIORITY_GET/etc are rejected at runtime, we will add explicit receipt-only branches next.")
    return True


def main() -> int:
    ok_schema = patch_schema_action_type_enum()
    ok_adapter = patch_engine_adapter_allowlist()
    ok_exec = patch_runtime_executor_receipts()

    if not ok_schema or not ok_adapter or not ok_exec:
        print("\nPATCH RESULT: NOT FULLY APPLIED (see errors above). No v1 was touched.")
        return 2

    print("\nPATCH RESULT: OK (v2 schema + adapter allowlist updated; executor left conservative if uncertain).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
