from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.common import current_utc_time


class SearchTask(BaseModel):
    query: str = Field(..., description="Target search query string")
    objective: str = Field(..., description="Specific evidence goal of this search")
    priority: int = Field(default=1, description="1 is highest priority")
    target_domains: List[str] = Field(default_factory=list, description="Preferred domains if any")
    rationale: str = Field(default="", description="Why this search is needed")


class SearchResultItem(BaseModel):
    title: str
    url: str
    snippet: str
    source_domain: str
    is_official: bool = False
    rank: int = 1
    query: str
    retrieved_at: datetime = Field(default_factory=current_utc_time)


class SearchResponse(BaseModel):
    query: str
    total_results: int
    items: List[SearchResultItem]
    search_engine: str = "google"
    error: Optional[str] = None
