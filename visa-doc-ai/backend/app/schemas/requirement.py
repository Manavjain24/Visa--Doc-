from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.common import (
    RequirementClassification,
    ClaimOutcome,
    current_utc_time
)


class ExtractedEvidence(BaseModel):
    id: str
    source_id: str
    source_url: str
    source_title: str
    is_official: bool
    exact_quote: str = Field(..., description="Verbatim text traceable to retrieved page")
    char_offset_start: int = 0
    char_offset_end: int = 0
    applicable_categories: List[str] = Field(default_factory=list)
    applicable_conditions: List[str] = Field(default_factory=list)
    extracted_at: datetime = Field(default_factory=current_utc_time)


class CandidateRequirement(BaseModel):
    id: str
    title: str
    description: str
    proposed_classification: RequirementClassification
    applicable_conditions: List[str] = Field(default_factory=list)
    exceptions: List[str] = Field(default_factory=list)
    supporting_evidence_ids: List[str] = Field(default_factory=list)


class ValidatedRequirement(BaseModel):
    id: str
    candidate_id: str
    title: str
    description: str
    classification: RequirementClassification
    verification_outcome: ClaimOutcome
    confidence_score: float = Field(ge=0.0, le=1.0)
    conditions: List[str] = Field(default_factory=list)
    exceptions: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    source_urls: List[str] = Field(default_factory=list)
    deterministic_rationale: str


class ConflictRecord(BaseModel):
    requirement_title: str
    issue: str
    source_a_url: str
    source_a_claim: str
    source_b_url: str
    source_b_claim: str
    resolution_strategy: str
