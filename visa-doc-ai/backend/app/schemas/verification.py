from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.common import RequirementClassification, ClaimOutcome
from app.schemas.visa_profile import ApplicantProfile
from app.schemas.requirement import ExtractedEvidence, ConflictRecord


class VerificationRequest(BaseModel):
    applicant_profile: ApplicantProfile
    claim_statement: str = Field(..., description="The visa document requirement claim to test")
    candidate_category: Optional[str] = None


class VerificationResult(BaseModel):
    claim_statement: str
    outcome: ClaimOutcome
    classification: RequirementClassification
    is_verified: bool
    rationale: str
    supporting_evidence: List[ExtractedEvidence] = Field(default_factory=list)
    conflicting_evidence: List[ConflictRecord] = Field(default_factory=list)
    sources_consulted: List[str] = Field(default_factory=list)
