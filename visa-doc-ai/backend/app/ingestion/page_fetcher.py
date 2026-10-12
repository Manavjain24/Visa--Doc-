import uuid
import httpx
from datetime import datetime, timezone
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import SecurityException, IngestionException
from app.schemas.source import RetrievedSource, SourceMetadata
from app.schemas.common import SourceTier
from app.utils.url_utils import extract_domain, is_official_domain, get_source_tier, normalize_url
from app.ingestion.url_validator import validate_url_or_raise
from app.ingestion.content_extractor import extract_content_from_html
from app.ingestion.pdf_extractor import extract_text_from_pdf


class PageFetcher:
    """Secure backend ingestion service for web and PDF sources."""

    def __init__(self, timeout: float = None, max_content_length: int = None):
        self.timeout = timeout or settings.INGESTION_TIMEOUT_SECONDS
        self.max_length = max_content_length or settings.INGESTION_MAX_CONTENT_LENGTH
        self.headers = {
            "User-Agent": settings.INGESTION_USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,application/pdf;q=0.8,*/*;q=0.7",
            "Accept-Language": "en-US,en;q=0.9",
        }

    async def fetch_source_async(self, url: str) -> RetrievedSource:
        source_id = str(uuid.uuid4())
        norm_url = normalize_url(url)
        domain = extract_domain(norm_url)
        is_official = is_official_domain(norm_url)
        tier = get_source_tier(norm_url)

        try:
            validate_url_or_raise(norm_url)
        except SecurityException as sec_err:
            logger.warning(f"Security validation blocked URL {norm_url}: {sec_err}")
            return RetrievedSource(
                id=source_id,
                metadata=SourceMetadata(
                    url=norm_url,
                    domain=domain,
                    is_official=is_official,
                    tier=tier,
                    http_status=403,
                    content_type="text/plain",
                ),
                raw_text="",
                is_accessible=False,
                error_message=f"Blocked by security boundary: {str(sec_err)}",
            )

        try:
            async with httpx.AsyncClient(
                headers=self.headers,
                timeout=self.timeout,
                follow_redirects=True,
                max_redirects=3,
                verify=False # avoid failing on strict government self-signed certs in test
            ) as client:
                response = await client.get(norm_url)

                if response.status_code >= 400:
                    return RetrievedSource(
                        id=source_id,
                        metadata=SourceMetadata(
                            url=norm_url,
                            domain=domain,
                            is_official=is_official,
                            tier=tier,
                            http_status=response.status_code,
                            content_type=response.headers.get("content-type", "text/plain"),
                        ),
                        raw_text="",
                        is_accessible=False,
                        error_message=f"HTTP {response.status_code}: {response.reason_phrase}",
                    )

                content_type = response.headers.get("content-type", "").lower()
                content_bytes = response.content

                if len(content_bytes) > self.max_length:
                    # Truncate content bytes safely
                    content_bytes = content_bytes[:self.max_length]

                if "application/pdf" in content_type or norm_url.lower().endswith(".pdf"):
                    raw_text, pdf_meta = extract_text_from_pdf(content_bytes)
                    title = pdf_meta.get("pdf_info", {}).get("/Title", f"PDF Document from {domain}")
                    had_inj = False
                    c_hash = ""
                else:
                    text_str = content_bytes.decode(response.encoding or "utf-8", errors="replace")
                    raw_text, title, had_inj, c_hash = extract_content_from_html(text_str)

                return RetrievedSource(
                    id=source_id,
                    metadata=SourceMetadata(
                        url=norm_url,
                        domain=domain,
                        title=title or f"Page from {domain}",
                        is_official=is_official,
                        tier=tier,
                        http_status=response.status_code,
                        content_type=content_type or "text/html",
                        content_hash=c_hash,
                    ),
                    raw_text=raw_text,
                    is_accessible=True,
                    had_injection_attempt=had_inj,
                )

        except Exception as e:
            logger.warning(f"Error fetching page {norm_url}: {e}")
            return RetrievedSource(
                id=source_id,
                metadata=SourceMetadata(
                    url=norm_url,
                    domain=domain,
                    is_official=is_official,
                    tier=tier,
                    http_status=0,
                    content_type="unknown",
                ),
                raw_text="",
                is_accessible=False,
                error_message=str(e),
            )

    def fetch_source(self, url: str) -> RetrievedSource:
        """Synchronous wrapper for fetch_source_async."""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # We are in an active event loop, run with nest_asyncio or httpx sync
                return self._fetch_sync(url)
            return loop.run_until_complete(self.fetch_source_async(url))
        except RuntimeError:
            return self._fetch_sync(url)

    def _fetch_sync(self, url: str) -> RetrievedSource:
        source_id = str(uuid.uuid4())
        norm_url = normalize_url(url)
        domain = extract_domain(norm_url)
        is_official = is_official_domain(norm_url)
        tier = get_source_tier(norm_url)

        try:
            validate_url_or_raise(norm_url)
        except SecurityException as sec_err:
            return RetrievedSource(
                id=source_id,
                metadata=SourceMetadata(
                    url=norm_url,
                    domain=domain,
                    is_official=is_official,
                    tier=tier,
                    http_status=403,
                    content_type="text/plain",
                ),
                raw_text="",
                is_accessible=False,
                error_message=f"Blocked by security boundary: {str(sec_err)}",
            )

        try:
            with httpx.Client(
                headers=self.headers,
                timeout=self.timeout,
                follow_redirects=True,
                max_redirects=3,
                verify=False
            ) as client:
                response = client.get(norm_url)
                if response.status_code >= 400:
                    return RetrievedSource(
                        id=source_id,
                        metadata=SourceMetadata(
                            url=norm_url,
                            domain=domain,
                            is_official=is_official,
                            tier=tier,
                            http_status=response.status_code,
                            content_type=response.headers.get("content-type", "text/plain"),
                        ),
                        raw_text="",
                        is_accessible=False,
                        error_message=f"HTTP {response.status_code}: {response.reason_phrase}",
                    )

                content_type = response.headers.get("content-type", "").lower()
                content_bytes = response.content[:self.max_length]

                if "application/pdf" in content_type or norm_url.lower().endswith(".pdf"):
                    raw_text, pdf_meta = extract_text_from_pdf(content_bytes)
                    title = pdf_meta.get("pdf_info", {}).get("/Title", f"PDF Document from {domain}")
                    had_inj = False
                    c_hash = ""
                else:
                    text_str = content_bytes.decode(response.encoding or "utf-8", errors="replace")
                    raw_text, title, had_inj, c_hash = extract_content_from_html(text_str)

                return RetrievedSource(
                    id=source_id,
                    metadata=SourceMetadata(
                        url=norm_url,
                        domain=domain,
                        title=title or f"Page from {domain}",
                        is_official=is_official,
                        tier=tier,
                        http_status=response.status_code,
                        content_type=content_type or "text/html",
                        content_hash=c_hash,
                    ),
                    raw_text=raw_text,
                    is_accessible=True,
                    had_injection_attempt=had_inj,
                )
        except Exception as e:
            return RetrievedSource(
                id=source_id,
                metadata=SourceMetadata(
                    url=norm_url,
                    domain=domain,
                    is_official=is_official,
                    tier=tier,
                    http_status=0,
                    content_type="unknown",
                ),
                raw_text="",
                is_accessible=False,
                error_message=str(e),
            )
