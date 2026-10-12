import hashlib
from typing import Tuple
from bs4 import BeautifulSoup
from app.utils.text_utils import clean_extracted_text
from app.core.security import sanitize_untrusted_text


def extract_content_from_html(html_str: str) -> Tuple[str, str, bool, str]:
    """
    Extracts readable text and title from HTML, removing non-content tags.
    Sanitizes untrusted text and flags injection attempts.
    Returns: (cleaned_text, title, had_injection, sha256_hash)
    """
    if not html_str:
        return "", "", False, ""

    content_hash = hashlib.sha256(html_str.encode('utf-8', errors='ignore')).hexdigest()

    soup = BeautifulSoup(html_str, "html.parser")

    # Extract title
    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()

    # Decompose script, style, navigation, footer, ads
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript", "svg", "form"]):
        tag.decompose()

    # Extract visible text
    raw_text = soup.get_text(separator="\n")
    cleaned = clean_extracted_text(raw_text)

    # Sanitize for prompt injection
    sanitized_text, had_injection = sanitize_untrusted_text(cleaned)

    return sanitized_text, title, had_injection, content_hash
