import time
from typing import Optional, Dict, Any, List
from serpapi import GoogleSearch

from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import SerpApiException
from app.schemas.search import SearchResponse, SearchResultItem
from app.search.base import BaseSearchProvider
from app.search.cache import search_cache
from app.search.result_normalizer import normalize_search_results


class SerpApiProvider(BaseSearchProvider):
    """
    Real SerpApi Google Search Provider.
    Executes search queries via the SerpApi API with caching, retry bounds,
    and credential validation.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        use_cache: bool = True
    ):
        self.api_key = api_key if api_key is not None else settings.SERPAPI_API_KEY
        self.timeout = timeout or settings.SERPAPI_TIMEOUT_SECONDS
        self.max_retries = max_retries if max_retries is not None else settings.SERPAPI_MAX_RETRIES
        self.use_cache = use_cache

    def search(self, query: str, num_results: int = 10) -> SearchResponse:
        """Executes a search via SerpApi, enforcing validation, caching, and retries."""
        if not query or not query.strip():
            return SearchResponse(query=query, total_results=0, items=[])

        query = query.strip()

        # Check Cache first
        if self.use_cache:
            cached = search_cache.get(query)
            if cached is not None:
                return cached

        # Validate credentials
        if not self.api_key or not self.api_key.strip():
            logger.error("SerpApi search attempted without an API key.")
            raise SerpApiException(
                "SerpApi credentials missing: SERPAPI_API_KEY is not configured in environment or .env file."
            )

        params: Dict[str, Any] = {
            "q": query,
            "engine": "google",
            "num": num_results,
            "api_key": self.api_key,
        }

        attempts = 0
        last_error: Optional[Exception] = None

        while attempts <= self.max_retries:
            attempts += 1
            try:
                logger.info(f"Executing SerpApi query (attempt {attempts}): '{query}'")
                search_client = GoogleSearch(params)
                result_dict = search_client.get_dict()

                # Handle SerpApi returned errors
                if "error" in result_dict:
                    err_msg = str(result_dict["error"])
                    if "Invalid API key" in err_msg or "Invalid api_key" in err_msg:
                        raise SerpApiException(f"Invalid SerpApi credentials: {err_msg}")
                    raise SerpApiException(f"SerpApi query error: {err_msg}")

                organic_results: List[Dict[str, Any]] = result_dict.get("organic_results", [])
                normalized_items = normalize_search_results(organic_results, query=query)

                response = SearchResponse(
                    query=query,
                    total_results=len(normalized_items),
                    items=normalized_items,
                    search_engine="google"
                )

                if self.use_cache:
                    search_cache.set(query, response)

                return response

            except SerpApiException:
                # Don't retry on fatal auth or bad query errors
                raise
            except Exception as e:
                last_error = e
                logger.warning(f"SerpApi request failed on attempt {attempts}: {e}")
                if attempts <= self.max_retries:
                    time.sleep(0.5 * attempts)

        logger.error(f"Exhausted all {self.max_retries + 1} attempts for query '{query}': {last_error}")
        raise SerpApiException(f"SerpApi search failed after {self.max_retries + 1} attempts: {str(last_error)}")
