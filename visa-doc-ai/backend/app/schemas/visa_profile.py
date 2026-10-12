from typing import List, Optional
from pydantic import BaseModel, Field


class ApplicantProfile(BaseModel):
    nationality: str = Field(..., description="Country of citizenship / passport")
    residence_country: str = Field(..., description="Current country of legal residence")
    destination_country: str = Field(..., description="Target travel destination country")
    visa_category: str = Field(..., description="Type of visa, e.g., Tourist, Business, Student, Work")
    purpose_of_travel: str = Field(..., description="Brief summary of travel purpose")
    planned_duration_days: int = Field(default=15, ge=1, le=3650, description="Length of planned stay in days")
    employment_status: str = Field(default="Employed", description="Employed, Self-Employed, Student, Retired, etc.")
    financial_sponsor: str = Field(default="Self", description="Source of funds: Self, Employer, Family sponsor, etc.")
    has_previous_visas: bool = Field(default=False, description="Whether applicant holds previous relevant visas")
    special_circumstances: List[str] = Field(default_factory=list, description="Minor, freelancer, traveling with family, etc.")
    specific_questions: List[str] = Field(default_factory=list, description="Specific questions the applicant asks")


class ApplicantProfileCreate(ApplicantProfile):
    pass


class ApplicantProfileResponse(ApplicantProfile):
    id: str
