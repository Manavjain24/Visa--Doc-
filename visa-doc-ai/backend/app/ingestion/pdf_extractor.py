import io
from typing import Tuple
from app.core.exceptions import IngestionException
from app.core.logging import logger

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


def extract_text_from_pdf(pdf_bytes: bytes) -> Tuple[str, dict]:
    """
    Extracts text and metadata from PDF bytes.
    Returns (extracted_text, metadata).
    """
    if not PdfReader:
        raise IngestionException("pypdf is not installed.")

    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        metadata = {
            "num_pages": len(reader.pages),
            "pdf_info": {k: str(v) for k, v in (reader.metadata or {}).items()}
        }
        
        extracted_pages = []
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            if page_text.strip():
                extracted_pages.append(f"[Page {i+1}]\n{page_text}")
                
        full_text = "\n\n".join(extracted_pages)
        return full_text, metadata
    except Exception as e:
        logger.warning(f"Failed to parse PDF bytes: {e}")
        raise IngestionException(f"Failed to extract PDF content: {str(e)}")
