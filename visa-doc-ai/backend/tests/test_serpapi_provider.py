from unittest.mock import patch, MagicMock
import pytest
from app.search.serpapi_provider import SerpApiProvider
from app.search.cache import search_cache
from app.core.exceptions import SerpApiException


def test_missing_credentials_raises_serpapi_exception():
    provider = SerpApiProvider(api_key="", use_cache=False)
    with pytest.raises(SerpApiException) as exc_info:
        provider.search("Germany tourist visa checklist")
    assert "credentials missing" in str(exc_info.value).lower()


def test_invalid_credentials_from_serpapi_response():
    provider = SerpApiProvider(api_key="invalid_test_key", use_cache=False, max_retries=0)
    
    with patch("app.search.serpapi_provider.GoogleSearch") as mock_search_cls:
        mock_instance = MagicMock()
        mock_instance.get_dict.return_value = {"error": "Invalid API key."}
        mock_search_cls.return_value = mock_instance
        
        with pytest.raises(SerpApiException) as exc_info:
            provider.search("Germany tourist visa")
        assert "invalid serpapi credentials" in str(exc_info.value).lower()


def test_successful_search_and_normalization(sample_search_json: dict):
    search_cache.clear()
    provider = SerpApiProvider(api_key="valid_mock_key", use_cache=True, max_retries=1)
    
    with patch("app.search.serpapi_provider.GoogleSearch") as mock_search_cls:
        mock_instance = MagicMock()
        mock_instance.get_dict.return_value = sample_search_json
        mock_search_cls.return_value = mock_instance
        
        resp = provider.search("Germany tourist visa checklist")
        assert resp.total_results == 3
        # First item should be official government domain (india.diplo.de)
        assert resp.items[0].is_official is True
        assert "india.diplo.de" in resp.items[0].url
        
        # Verify search caching prevents second call
        mock_search_cls.reset_mock()
        cached_resp = provider.search("Germany tourist visa checklist")
        assert cached_resp.total_results == 3
        mock_search_cls.assert_not_called()


def test_serpapi_retries_and_failure():
    search_cache.clear()
    provider = SerpApiProvider(api_key="valid_mock_key", use_cache=False, max_retries=2)
    
    with patch("app.search.serpapi_provider.GoogleSearch") as mock_search_cls:
        mock_search_cls.side_effect = Exception("Connection timed out")
        
        with pytest.raises(SerpApiException) as exc_info:
            provider.search("Germany tourist visa checklist")
            
        assert "failed after 3 attempts" in str(exc_info.value).lower()
