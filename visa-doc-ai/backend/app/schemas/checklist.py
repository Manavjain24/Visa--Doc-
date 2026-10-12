from datetime import datetime
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from app.schemas.common import RequirementClassification, current_utc_time


class ChecklistCitation(BaseModel):
    source_title: str
    source_url: str
    quote: str
    is_official: bool = True


class ChecklistItem(BaseModel):
    id: str
    title: str
    description: str
    classification: RequirementClassification
    applies_to: str
    conditions: List[str] = Field(default_factory=list)
    exceptions: List[str] = Field(default_factory=list)
    citations: List[ChecklistCitation] = Field(default_factory=list)
    is_actionable: bool = True


class DocumentChecklist(BaseModel):
    id: str
    run_id: str
    destination_country: str
    visa_category: str
    applicant_summary: str
    mandatory_items: List[ChecklistItem] = Field(default_factory=list)
    conditional_items: List[ChecklistItem] = Field(default_factory=list)
    recommended_items: List[ChecklistItem] = Field(default_factory=list)
    unverified_items: List[ChecklistItem] = Field(default_factory=list)
    unresolved_questions: List[str] = Field(default_factory=list)
    disclaimer: str = (
        "IMPORTANT LEGAL DISCLAIMER: This document checklist is generated through automated "
        "evidence-backed research from official immigration authorities. It is provided for informational "
        "purposes only and DOES NOT constitute legal advice or guarantee visa approval. Consular officers "
        "possess final discretion on document requirements and visa adjudication."
    )
    generated_at: datetime = Field(default_factory=current_utc_time)
