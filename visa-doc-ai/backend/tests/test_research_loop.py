import pytest
from unittest.mock import MagicMock, patch
from app.schemas.visa_profile import ApplicantProfile
from app.schemas.search import SearchResponse, SearchResultItem
from app.schemas.source import RetrievedSource, SourceMetadata
from app.schemas.common import SourceTier, RequirementClassification, ResearchStatus
from app.services.research_orchestrator import ResearchOrchestrator
from app.schemas.research import ResearchState
from app.search.base import BaseSearchProvider
from app.ingestion.page_fetcher import PageFetcher


class MockTestSearchProvider(BaseSearchProvider):
    """Custom search provider for testing loop behaviors."""
    def __init__(self, items=None, fail_query=None):
        self.items = items or []
        self.fail_query = fail_query
        self.searches_called = []

    def search(self, query: str, num_results: int = 10) -> SearchResponse:
        self.searches_called.append(query)
        if self.fail_query and self.fail_query in query:
            raise Exception("Search API service unavailable")
        return SearchResponse(
            query=query,
            total_results=len(self.items),
            items=self.items,
            search_engine="google"
        )


class MockTestPageFetcher(PageFetcher):
    """Custom fetcher providing controlled HTML fixtures."""
    def __init__(self, html_map=None, inaccessible_urls=None):
        super().__init__()
        self.html_map = html_map or {}
        self.inaccessible_urls = inaccessible_urls or set()

    def fetch_source(self, url: str) -> RetrievedSource:
        if url in self.inaccessible_urls:
            return RetrievedSource(
                id="inaccessible_src",
                metadata=SourceMetadata(url=url, domain="test.gov", is_official=True, http_status=404),
                raw_text="",
                is_accessible=False,
                error_message="HTTP 404 Not Found"
            )
        html_content = self.html_map.get(url, "<p>Standard page</p>")
        from app.ingestion.content_extractor import extract_content_from_html
        text, title, had_inj, c_hash = extract_content_from_html(html_content)
        return RetrievedSource(
            id="mock_src_id",
            metadata=SourceMetadata(url=url, domain="diplo.de", title=title, is_official=True, tier=SourceTier.OFFICIAL),
            raw_text=text,
            is_accessible=True,
            had_injection_attempt=had_inj
        )


def test_full_successful_research_run(sample_profile: ApplicantProfile, sample_html: str):
    official_url = "https://india.diplo.de/checklist"
    search_item = SearchResultItem(
        title="Official Checklist - German Missions",
        url=official_url,
        snippet="Valid passport, travel health insurance with 30,000 EUR coverage, 3 months bank statements.",
        source_domain="india.diplo.de",
        is_official=True,
        rank=1,
        query="Germany tourist visa"
    )

    search_provider = MockTestSearchProvider(items=[search_item])
    fetcher = MockTestPageFetcher(html_map={official_url: sample_html})

    orchestrator = ResearchOrchestrator(search_provider=search_provider, page_fetcher=fetcher)

    initial_state = ResearchState(
        run_id="run_success_1",
        applicant_profile=sample_profile,
        max_iterations=3,
        max_search_budget=5,
        search_budget_remaining=5
    )

    final_state = orchestrator.run(initial_state)

    assert final_state.workflow_status == ResearchStatus.COMPLETED
    assert final_state.final_checklist is not None
    assert len(final_state.final_checklist.mandatory_items) > 0
    # Must have extracted evidence from the official page
    assert len(final_state.extracted_evidence) > 0
    # Provenance verification: citations must match
    assert any(c.source_url == official_url for item in final_state.final_checklist.mandatory_items for c in item.citations)
    # Check observability traces
    assert len(final_state.traces) >= 4
    stages = [t.stage for t in final_state.traces]
    assert "Planning" in stages
    assert "Search" in stages
    assert "Evidence Extraction" in stages
    assert "Verification" in stages
    assert "Checklist Generation" in stages


def test_inaccessible_source_pages_handling(sample_profile: ApplicantProfile):
    broken_url = "https://broken-server.gov/down"
    search_item = SearchResultItem(
        title="Broken Document",
        url=broken_url,
        snippet="Snippet text",
        source_domain="broken-server.gov",
        is_official=True,
        rank=1,
        query="test query"
    )

    search_provider = MockTestSearchProvider(items=[search_item])
    fetcher = MockTestPageFetcher(inaccessible_urls={broken_url})

    orchestrator = ResearchOrchestrator(search_provider=search_provider, page_fetcher=fetcher)
    initial_state = ResearchState(
        run_id="run_inaccessible_1",
        applicant_profile=sample_profile,
        max_iterations=2,
        max_search_budget=3
    )

    final_state = orchestrator.run(initial_state)

    # Workflow must not crash; should handle inaccessible page and record error/warning
    assert final_state.workflow_status == ResearchStatus.COMPLETED
    assert any("inaccessible" in err.lower() for err in final_state.errors_and_warnings)


def test_research_loop_reaches_iteration_limit(sample_profile: ApplicantProfile):
    # Empty search results will keep questions unresolved, exercising loop bounds
    search_provider = MockTestSearchProvider(items=[])
    fetcher = MockTestPageFetcher()

    orchestrator = ResearchOrchestrator(search_provider=search_provider, page_fetcher=fetcher)
    initial_state = ResearchState(
        run_id="run_iter_limit_1",
        applicant_profile=sample_profile,
        max_iterations=2,
        max_search_budget=10
    )

    final_state = orchestrator.run(initial_state)

    assert final_state.workflow_status == ResearchStatus.COMPLETED
    assert "Maximum research iterations reached" in (final_state.stop_reason or "") or "Duplicate-query" in (final_state.stop_reason or "")


def test_search_budget_exhaustion(sample_profile: ApplicantProfile):
    search_provider = MockTestSearchProvider(items=[])
    fetcher = MockTestPageFetcher()

    orchestrator = ResearchOrchestrator(search_provider=search_provider, page_fetcher=fetcher)
    initial_state = ResearchState(
        run_id="run_budget_exhaust_1",
        applicant_profile=sample_profile,
        max_iterations=5,
        max_search_budget=1,
        search_budget_remaining=1
    )

    final_state = orchestrator.run(initial_state)

    assert final_state.workflow_status == ResearchStatus.COMPLETED
    assert final_state.search_budget_remaining <= 0
    assert "Search request budget exhausted" in (final_state.stop_reason or "") or "Maximum research iterations" in (final_state.stop_reason or "")


def test_duplicate_search_prevention(sample_profile: ApplicantProfile):
    # Query executed already
    search_provider = MockTestSearchProvider(items=[])
    fetcher = MockTestPageFetcher()

    orchestrator = ResearchOrchestrator(search_provider=search_provider, page_fetcher=fetcher)
    initial_state = ResearchState(
        run_id="run_dup_1",
        applicant_profile=sample_profile,
        max_iterations=2,
        max_search_budget=5
    )

    final_state = orchestrator.run(initial_state)
    queries = final_state.executed_queries
    # Verify no duplicate queries executed
    assert len(queries) == len(set(queries))
