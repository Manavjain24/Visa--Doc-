from abc import ABC, abstractmethod
from typing import Optional
from app.schemas.search import SearchResponse


class BaseSearchProvider(ABC):
    """Abstract interface for web search providers."""

    @abstractmethod
    def search(self, query: str, num_results: int = 10) -> SearchResponse:
        """Executes a search query and returns normalized results."""
        pass
