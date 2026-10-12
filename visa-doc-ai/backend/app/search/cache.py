from typing import Dict, Optional
import time
from app.schemas.search import SearchResponse
from app.core.logging import logger


class SearchCache:
    """Thread-safe in-memory cache with optional TTL for search responses."""

    def __init__(self, ttl_seconds: int = 3600):
        self._cache: Dict[str, SearchResponse] = {}
        self._timestamps: Dict[str, float] = {}
        self.ttl_seconds = ttl_seconds

    def _normalize_key(self, query: str) -> str:
        return " ".join(query.strip().lower().split())

    def get(self, query: str) -> Optional[SearchResponse]:
        key = self._normalize_key(query)
        if key in self._cache:
            created_at = self._timestamps.get(key, 0)
            if time.time() - created_at < self.ttl_seconds:
                logger.info(f"Search cache HIT for query: '{query}'")
                return self._cache[key]
            else:
                logger.debug(f"Search cache EXPIRED for query: '{query}'")
                del self._cache[key]
                del self._timestamps[key]
        return None

    def set(self, query: str, response: SearchResponse) -> None:
        key = self._normalize_key(query)
        self._cache[key] = response
        self._timestamps[key] = time.time()

    def has_seen(self, query: str) -> bool:
        key = self._normalize_key(query)
        return key in self._cache

    def clear(self) -> None:
        self._cache.clear()
        self._timestamps.clear()


search_cache = SearchCache()
