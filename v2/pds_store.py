from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any, Dict, Optional


def _today_local_ymd() -> str:
    return time.strftime("%Y-%m-%d", time.localtime())


def _default_dir() -> Path:
    root = Path(__file__).resolve().parents[1]
    return root / "v2" / "_pds"


def pds_dir() -> Path:
    override = os.environ.get("VERA_V2_PDS_DIR", "").strip()
    if override:
        return Path(override).expanduser().resolve()
    return _default_dir()


def pds_path(date_ymd: Optional[str] = None) -> Path:
    d = pds_dir()
    ymd = (date_ymd or _today_local_ymd()).strip()
    return d / (ymd + ".json")


def load_pds(date_ymd: Optional[str] = None) -> Dict[str, Any]:
    fp = pds_path(date_ymd)
    try:
        if not fp.exists():
            return {}
        data = json.loads(fp.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_pds(pds: Dict[str, Any], date_ymd: Optional[str] = None) -> Path:
    if pds is None or not isinstance(pds, dict):
        pds = {}

    fp = pds_path(date_ymd)
    fp.parent.mkdir(parents=True, exist_ok=True)

    tmp = fp.with_suffix(fp.suffix + ".tmp")
    payload = json.dumps(pds, ensure_ascii=False, indent=2, sort_keys=True)

    tmp.write_text(payload + "\n", encoding="utf-8")
    tmp.replace(fp)
    return fp
