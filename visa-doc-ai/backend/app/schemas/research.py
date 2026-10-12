from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from app.schemas.common import ResearchStatus, current_utc_time
from app.schemas.visa_profile import ApplicantProfile
from app.schemas.search import SearchTask, SearchResultItem
from app.schemas.source import RetrievedSource
from app.schemas.requirement import (
    ExtractedEvidence,
    CandidateRequirement,
    ValidatedRequirement,
    ConflictRecord
)
from app.schemas.checklist import DocumentChecklist


class ResearchTraceEntry(BaseModel):
    id: str
    timestamp: datetime = Field(default_factory=current_utc_time)
    stage: str
    agent_name: str
    action: str
    summary: str
    details: Dict[str, Any] = Field(default_factory=dict)
    evidence_ids: List[str] = Field(default_factory=list)
    source_urls: List[str] = Field(default_factory=list)


class ResearchRunCreate(BaseModel):
    applicant_profile: ApplicantProfile
    user_question: Optional[str] = ""
    max_iterations: Optional[int] = 3
    max_search_budget: Optional[int] = 5


class ResearchState(BaseModel):
    run_id: str
    applicant_profile: ApplicantProfile
    user_question: str = ""
    
    # Planning & Objectives
    research_objectives: List[str] = Field(default_factory=list)
    planned_search_tasks: List[SearchTask] = Field(default_factory=list)
    executed_queries: List[str] = Field(default_factory=list)
    
    # Evidence & Sources
    search_results: List[SearchResultItem] = Field(default_factory=list)
    retrieved_sources: List[RetrievedSource] = Field(default_factory=list)
    extracted_evidence: List[ExtractedEvidence] = Field(default_factory=list)
    
    # Verification & Reasoning
    candidate_requirements: List[CandidateRequirement] = Field(default_factory=list)
    validated_classifications: List[ValidatedRequirement] = Field(default_factory=list)
    unresolved_questions: List[str] = Field(default_factory=list)
    conflicting_evidence: List[ConflictRecord] = Field(default_factory=list)
    
    # Execution Bounding & Budget
    iteration_count: int = 0
    max_iterations: int = 3
    search_budget_remaining: int = 5
    max_search_budget: int = 5
    stop_reason: Optional[str] = None
    
    # Errors & Observability
    errors_and_warnings: List[str] = Field(default_factory=list)
    traces: List[ResearchTraceEntry] = Field(default_factory=list)
    
    # Output & Lifecycle
    final_checklist: Optional[DocumentChecklist] = None
    workflow_status: ResearchStatus = ResearchStatus.INITIALIZING
    created_at: datetime = Field(default_factory=current_utc_time)
    updated_at: datetime = Field(default_factory=current_utc_time)


class ResearchRunSummary(BaseModel):
    run_id: str
    workflow_status: ResearchStatus
    iteration_count: int
    search_budget_remaining: int
    objectives_count: int
    sources_count: int
    evidence_count: int
    validated_requirements_count: int
    unresolved_questions_count: int
    stop_reason: Optional[str] = None
    has_checklist: bool = False
    created_at: datetime
    updated_at: datetime
