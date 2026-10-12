from app.ingestion.content_extractor import extract_content_from_html
from app.utils.text_utils import find_quote_offsets
from app.ingestion.url_validator import is_safe_url


def test_html_content_extraction(sample_html: str):
    text, title, had_injection, c_hash = extract_content_from_html(sample_html)
    
    assert "Federal Foreign Office" in title
    assert "Travel Health Insurance" in text
    assert "minimum coverage of 30,000 EUR" in text
    assert "Personal original bank account statements" in text
    assert len(c_hash) == 64
    
    # Prompt injection test within webpage
    assert had_injection is True
    assert "REDACTED_UNTRUSTED_INSTRUCTION" in text
    assert "Ignore all previous instructions" not in text


def test_quote_offset_matching(sample_html: str):
    text, _, _, _ = extract_content_from_html(sample_html)
    quote = "minimum coverage of 30,000 EUR"
    
    start, end = find_quote_offsets(text, quote)
    assert start != -1
    assert end > start
    assert text[start:end] == quote


def test_url_ssrf_validator():
    assert is_safe_url("https://india.diplo.de/visa") is True
    assert is_safe_url("http://127.0.0.1/admin") is False
    assert is_safe_url("http://localhost:8000") is False
    assert is_safe_url("ftp://ftp.diplo.de/files") is False
    assert is_safe_url("javascript:alert(1)") is False
