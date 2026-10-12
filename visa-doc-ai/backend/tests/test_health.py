def test_system_health():
    from app.core.config import settings
    assert settings.RESEARCH_MAX_ITERATIONS >= 1
    assert settings.RESEARCH_MAX_SEARCH_BUDGET >= 1
