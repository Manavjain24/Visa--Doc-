from typing import List, Dict, Any, Set
from app.schemas.search import SearchResultItem
from app.utils.url_utils import normalize_url, extract_domain, is_official_domain
from app.schemas.common import current_utc_time


def normalize_search_results(raw_results: List[Dict[str, Any]], query: str) -> List[SearchResultItem]:
    """
    Normalizes and deduplicates search items from raw search providers.
    Annotates whether each source is an official government/consulate domain.
    Does NOT classify document requirement status from snippets.
    """
    seen_urls: Set[str] = set()
    normalized_items: List[SearchResultItem] = []

    for rank, item in enumerate(raw_results, start=1):
        raw_url = item.get("link") or item.get("url") or ""
        if not raw_url:
            continue

        clean_url = normalize_url(raw_url)
        if clean_url in seen_urls:
            continue
        seen_urls.add(clean_url)

        domain = extract_domain(clean_url)
        official = is_official_domain(clean_url)
        title = item.get("title") or f"Document from {domain}"
        snippet = item.get("snippet") or item.get("description") or ""

        normalized_items.append(
            SearchResultItem(
                title=title,
                url=clean_url,
                snippet=snippet,
                source_domain=domain,
                is_official=official,
                rank=rank,
                query=query,
                retrieved_at=current_utc_time()
            )
        )

    # Sort prioritizing official sources first, maintaining ranking within tier
    normalized_items.sort(key=lambda x: (not x.is_official, x.rank))
    return normalized_items
