import time
from typing import Any, Dict, Optional

class TTLCache:
    """
    Simple in-memory TTL cache.
    """
    def __init__(self, default_ttl_seconds: int = 600):
        self.default_ttl = default_ttl_seconds
        self._store: Dict[str, Dict[str, Any]] = {}

    def get(self, key: str) -> Optional[Any]:
        item = self._store.get(key)
        if not item:
            return None
        if time.time() > item["expires_at"]:
            self._store.pop(key, None)
            return None
        return item["value"]

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
        self._store[key] = {"value": value, "expires_at": time.time() + ttl}

    def clear(self) -> None:
        self._store.clear()

