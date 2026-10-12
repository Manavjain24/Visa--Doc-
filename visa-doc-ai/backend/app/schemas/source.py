from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.common import SourceTier, current_utc_time


class SourceMetadata(BaseModel):
    url: str
    domain: str
    title: str = ""
    is_official: bool = False
    tier: SourceTier = SourceTier.GENERAL
    http_status: int = 200
    content_type: str = "text/html"
    retrieved_at: datetime = Field(default_factory=current_utc_time)
    content_hash: str = ""


class RetrievedSource(BaseModel):
    id: str
    metadata: SourceMetadata
    raw_text: str = ""
    summary: Optional[str] = None
    is_accessible: bool = True
    error_message: Optional[str] = None
    had_injection_attempt: bool = False
