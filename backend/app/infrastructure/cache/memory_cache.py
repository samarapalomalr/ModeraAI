import time
from typing import Optional

from app.domain.interfaces.result_cache import ResultCache


class InMemoryResultCache(ResultCache):
    """Cache em memória com TTL (evita refazer Apify + Gemini para o mesmo link)."""

    def __init__(self, ttl_seconds: int = 600):
        self._ttl = ttl_seconds
        self._items: dict[str, tuple[float, dict]] = {}

    def get(self, key: str) -> Optional[dict]:
        item = self._items.get(key)
        if not item:
            return None
        saved_at, value = item
        if time.time() - saved_at > self._ttl:
            self._items.pop(key, None)
            return None
        return value

    def set(self, key: str, value: dict) -> None:
        self._items[key] = (time.time(), value)
