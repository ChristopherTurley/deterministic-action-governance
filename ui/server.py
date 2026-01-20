\
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from jsonschema import Draft202012Validator

APP = FastAPI(title="DAG Sidecar Admin UI", version="1.0.0")

def _is_api_path(path: str) -> bool:
    return path.startswith("/api/")

def _extract_bearer(auth_header: str) -> str:
    if not auth_header:
        return ""
    m = re.match(r"^\s*Bearer\s+(.+?)\s*$", auth_header)
    return m.group(1) if m else ""

@APP.middleware("http")
async def _auth_middleware(request: Request, call_next):
    # Public: UI shell + static assets
    if not _is_api_path(request.url.path):
        return await call_next(request)

    # If UI_ADMIN_TOKEN is unset, fail closed (auditor-friendly)
    if not UI_ADMIN_TOKEN:
        return JSONResponse(status_code=503, content={"detail": "UI_ADMIN_TOKEN not configured"})

    token = _extract_bearer(request.headers.get("authorization", ""))
    if token != UI_ADMIN_TOKEN:
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

    return await call_next(request)


# -------- Config (fail-closed defaults) --------
SIDECAR_BASE_URL = os.getenv("SIDECAR_BASE_URL", "").strip()
POLICY_PATH = os.getenv("POLICY_PATH", "enterprise_sidecar/policy/policy_v1.example.json").strip()
RECEIPTS_DIR = os.getenv("RECEIPTS_DIR", "ui/runtime/receipts").strip()
READ_ONLY = os.getenv("READ_ONLY", "1").strip() != "0"
UI_ADMIN_TOKEN = os.getenv("UI_ADMIN_TOKEN", "").strip()

REPO_ROOT = Path(__file__).resolve().parents[1]  # repo root (ui/server.py -> repo/)
POLICY_FILE = (REPO_ROOT / POLICY_PATH).resolve()
RECEIPTS_PATH = (REPO_ROOT / RECEIPTS_DIR).resolve()

SCHEMA_POLICY_FILE = (REPO_ROOT / "enterprise_sidecar/schema/sidecar_policy_schema_v1.json").resolve()

# Guard: keep all file operations inside repo root
def _ensure_within_repo(p: Path) -> Path:
    try:
        p.relative_to(REPO_ROOT)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Path escapes repo root") from e
    return p

_ensure_within_repo(POLICY_FILE)
_ensure_within_repo(RECEIPTS_PATH)
_ensure_within_repo(SCHEMA_POLICY_FILE)

def _load_json(path: Path) -> Any:
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Missing file: {path.relative_to(REPO_ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {path.name}") from e

def _sha256_hex_bytes(b: bytes) -> str:
    h = hashlib.sha256()
    h.update(b)
    return h.hexdigest()

def _sha256_hex_json(obj: Any) -> str:
    # Deterministic canonical-ish encoding: sorted keys, compact separators.
    b = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return _sha256_hex_bytes(b)

def _load_policy_schema() -> Dict[str, Any]:
    return _load_json(SCHEMA_POLICY_FILE)

def _validate_policy(policy: Dict[str, Any]) -> Tuple[bool, List[str]]:
    schema = _load_policy_schema()
    v = Draft202012Validator(schema)
    errors = sorted(v.iter_errors(policy), key=lambda e: e.path)
    if not errors:
        return True, []
    msgs = []
    for e in errors[:50]:
        loc = "/".join([str(x) for x in e.path]) if e.path else "(root)"
        msgs.append(f"{loc}: {e.message}")
    return False, msgs

def _sidecar_get(path: str) -> Optional[Dict[str, Any]]:
    if not SIDECAR_BASE_URL:
        return None
    url = SIDECAR_BASE_URL.rstrip("/") + path
    try:
        r = requests.get(url, timeout=2.0)
        return {"ok": r.ok, "status": r.status_code, "json": (r.json() if r.headers.get("content-type","").startswith("application/json") else None)}
    except Exception as e:
        return {"ok": False, "status": 0, "error": str(e)}

# -------- Static UI --------
APP.mount("/static", StaticFiles(directory=str((Path(__file__).parent / "web").resolve())), name="static")

@APP.get("/", response_class=HTMLResponse)
def index() -> str:
    index_file = (Path(__file__).parent / "web" / "index.html").resolve()
    return index_file.read_text(encoding="utf-8")

@APP.get("/favicon.ico")
def favicon():
    return FileResponse(str((Path(__file__).parent / "web" / "favicon.svg").resolve()), media_type="image/svg+xml")

# -------- API: Status --------
@APP.get("/api/status")
def api_status() -> Dict[str, Any]:
    # Local policy info (hash/version)
    policy = _load_json(POLICY_FILE)
    policy_hash = _sha256_hex_json(policy)
    policy_version = policy.get("policy_version", "unknown")
    policy_id = policy.get("policy_id", "unknown")

    # Sidecar live endpoints (optional)
    health = _sidecar_get("/healthz")
    version = _sidecar_get("/version")

    # Latency quick stats from receipts
    RECEIPTS_PATH.mkdir(parents=True, exist_ok=True)
    latencies = []
    for p in sorted(RECEIPTS_PATH.glob("*.json"))[-200:]:
        try:
            obj = json.loads(p.read_text(encoding="utf-8"))
            lm = obj.get("latency_ms")
            if isinstance(lm, int):
                latencies.append(lm)
        except Exception:
            continue
    latencies.sort()
    def pct(q: float) -> Optional[int]:
        if not latencies:
            return None
        idx = int(round((len(latencies)-1) * q))
        return latencies[max(0, min(idx, len(latencies)-1))]

    return {
        "read_only": READ_ONLY,
        "policy": {
            "policy_id": policy_id,
            "policy_version": policy_version,
            "policy_hash": policy_hash,
            "policy_path": str(POLICY_FILE.relative_to(REPO_ROOT)),
        },
        "sidecar": {
            "base_url": SIDECAR_BASE_URL or None,
            "healthz": health,
            "version": version,
        },
        "latency_ms": {
            "count": len(latencies),
            "p50": pct(0.50),
            "p95": pct(0.95),
            "p99": pct(0.99),
        },
    }

# -------- API: Policy --------
@APP.get("/api/policy")
def api_policy_get() -> Dict[str, Any]:
    policy = _load_json(POLICY_FILE)
    ok, errors = _validate_policy(policy)
    return {
        "path": str(POLICY_FILE.relative_to(REPO_ROOT)),
        "policy": policy,
        "policy_hash": _sha256_hex_json(policy),
        "valid": ok,
        "validation_errors": errors,
        "read_only": READ_ONLY,
    }

@APP.post("/api/policy/validate")
def api_policy_validate(body: Dict[str, Any]) -> Dict[str, Any]:
    if "policy" not in body:
        raise HTTPException(status_code=400, detail="Missing 'policy' in body")
    policy = body["policy"]
    if not isinstance(policy, dict):
        raise HTTPException(status_code=400, detail="'policy' must be an object")
    ok, errors = _validate_policy(policy)
    return {
        "valid": ok,
        "validation_errors": errors,
        "policy_hash": _sha256_hex_json(policy),
    }

@APP.put("/api/policy")
def api_policy_put(body: Dict[str, Any]) -> Dict[str, Any]:
    if READ_ONLY:
        raise HTTPException(status_code=403, detail="READ_ONLY mode enabled")
    if "policy" not in body:
        raise HTTPException(status_code=400, detail="Missing 'policy' in body")
    policy = body["policy"]
    if not isinstance(policy, dict):
        raise HTTPException(status_code=400, detail="'policy' must be an object")

    ok, errors = _validate_policy(policy)
    if not ok:
        return JSONResponse(status_code=400, content={"valid": False, "validation_errors": errors})

    # Atomic write
    POLICY_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = POLICY_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(policy, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(POLICY_FILE)

    return {
        "ok": True,
        "path": str(POLICY_FILE.relative_to(REPO_ROOT)),
        "policy_hash": _sha256_hex_json(policy),
    }

# -------- API: Receipts --------
def _safe_receipt_path(receipt_name: str) -> Path:
    # Only allow filename-like ids ending with .json; prevent traversal.
    if "/" in receipt_name or "\\" in receipt_name or ".." in receipt_name:
        raise HTTPException(status_code=400, detail="Invalid receipt name")
    if not receipt_name.endswith(".json"):
        raise HTTPException(status_code=400, detail="Receipt must end with .json")
    p = (RECEIPTS_PATH / receipt_name).resolve()
    _ensure_within_repo(p)
    if p.parent != RECEIPTS_PATH:
        raise HTTPException(status_code=400, detail="Invalid receipt path")
    return p

@APP.get("/api/receipts")
def api_receipts_list(limit: int = 200) -> Dict[str, Any]:
    RECEIPTS_PATH.mkdir(parents=True, exist_ok=True)
    files = sorted(RECEIPTS_PATH.glob("*.json"), reverse=True)[: max(1, min(limit, 1000))]
    items = []
    for p in files:
        try:
            obj = json.loads(p.read_text(encoding="utf-8"))
            items.append({
                "file": p.name,
                "timestamp_utc": obj.get("timestamp_utc"),
                "decision": (obj.get("decision") or {}).get("status") if isinstance(obj.get("decision"), dict) else obj.get("decision"),
                "refusal_code": (obj.get("decision") or {}).get("refusal_code") if isinstance(obj.get("decision"), dict) else obj.get("refusal_code"),
                "rule_ids": (obj.get("decision") or {}).get("rule_ids") if isinstance(obj.get("decision"), dict) else obj.get("rule_ids"),
                "receipt_id": obj.get("receipt_id"),
                "policy_version": (obj.get("policy") or {}).get("policy_version") if isinstance(obj.get("policy"), dict) else obj.get("policy_version"),
                "latency_ms": obj.get("latency_ms"),
            })
        except Exception:
            items.append({"file": p.name, "parse_error": True})
    return {"dir": str(RECEIPTS_PATH.relative_to(REPO_ROOT)), "items": items}

@APP.get("/api/receipts/{receipt_file}")
def api_receipt_get(receipt_file: str) -> Dict[str, Any]:
    p = _safe_receipt_path(receipt_file)
    obj = _load_json(p)
    return {"file": p.name, "receipt": obj}

@APP.get("/api/receipts/{receipt_file}/download")
def api_receipt_download(receipt_file: str):
    p = _safe_receipt_path(receipt_file)
    return FileResponse(str(p), media_type="application/json", filename=p.name)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:APP", host="127.0.0.1", port=8080, reload=False)
