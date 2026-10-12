import os
import json
from pathlib import Path
import pytest
from app.schemas.visa_profile import ApplicantProfile

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_search_json() -> dict:
    with open(FIXTURES_DIR / "search_results.json", "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def sample_html() -> str:
    with open(FIXTURES_DIR / "sample_official_page.html", "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def sample_profile() -> ApplicantProfile:
    return ApplicantProfile(
        nationality="India",
        residence_country="India",
        destination_country="Germany",
        visa_category="Tourist",
        purpose_of_travel="Vacation and sightseeing in Berlin and Munich",
        planned_duration_days=14,
        employment_status="Employed",
        financial_sponsor="Self",
        has_previous_visas=False,
        special_circumstances=[],
        specific_questions=["What is the required duration for bank statements?"]
    )
