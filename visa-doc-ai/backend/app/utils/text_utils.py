import re
from typing import Tuple, List


def clean_extracted_text(text: str) -> str:
    """Cleans up excess whitespace, normalizing line breaks and spaces."""
    if not text:
        return ""
    # Normalize multiple newlines to double newline
    text = re.sub(r'\r\n|\r', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Normalize excessive spaces/tabs on single line
    text = re.sub(r'[ \t]{2,}', ' ', text)
    return text.strip()


def find_quote_offsets(full_text: str, quote: str) -> Tuple[int, int]:
    """
    Finds exact character offsets (start, end) of a quote in full_text.
    Falls back to case-insensitive match or normalized whitespace match.
    Returns (-1, -1) if not found.
    """
    if not full_text or not quote:
        return -1, -1
        
    # Exact match first
    idx = full_text.find(quote)
    if idx != -1:
        return idx, idx + len(quote)
        
    # Case-insensitive match
    lower_text = full_text.lower()
    lower_quote = quote.lower()
    idx = lower_text.find(lower_quote)
    if idx != -1:
        return idx, idx + len(quote)

    # Whitespace-collapsed match
    collapsed_quote = re.sub(r'\s+', ' ', quote.strip())
    # Try finding sub-chunks
    if len(collapsed_quote) > 20:
        prefix = collapsed_quote[:30]
        prefix_idx = lower_text.find(prefix.lower())
        if prefix_idx != -1:
            end_guess = min(len(full_text), prefix_idx + len(quote))
            return prefix_idx, end_guess
            
    return -1, -1


def chunk_text(text: str, chunk_size: int = 1500, overlap: int = 200) -> List[str]:
    """Splits long text into overlapping chunks for processing."""
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        chunks.append(chunk)
        if end == len(text):
            break
        start += (chunk_size - overlap)
    return chunks
