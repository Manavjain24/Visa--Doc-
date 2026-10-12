from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from app.core.config import settings
from app.core.logging import logger
from app.schemas.visa_profile import ApplicantProfile
from app.schemas.search import SearchTask
from app.schemas.requirement import CandidateRequirement, ValidatedRequirement


class BaseAIProvider(ABC):
    """Abstract interface for AI/LLM providers."""

    @abstractmethod
    def generate_plan(self, profile: ApplicantProfile, user_question: str, gaps: List[str]) -> Dict[str, Any]:
        """Generates research objectives and targeted search tasks."""
        pass

    @abstractmethod
    def generate_checklist_summary(self, validated_items: List[ValidatedRequirement], profile: ApplicantProfile) -> str:
        """Generates tailored guidance summary for the checklist."""
        pass


class MockAIProvider(BaseAIProvider):
    """
    Deterministic provider that generates verified structures without external network LLMs.
    Ensures tests and offline executions always succeed deterministically.
    """

    def generate_plan(self, profile: ApplicantProfile, user_question: str, gaps: List[str]) -> Dict[str, Any]:
        dest = profile.destination_country
        cat = profile.visa_category
        objectives = [
            f"Verify official mandatory travel document and passport criteria for {dest} {cat} visa.",
            f"Determine proof of financial sufficiency requirements for {profile.nationality} citizen residing in {profile.residence_country}.",
            f"Identify medical insurance specifications (coverage sum and geographic validity).",
            f"Verify occupational requirements for {profile.employment_status} status.",
        ]
        if user_question:
            objectives.append(f"Investigate specific user inquiry: {user_question}")

        return {
            "objectives": objectives,
            "relevant_conditions": [
                f"Applicant is {profile.employment_status}",
                f"Sponsorship: {profile.financial_sponsor}",
                f"Stay duration: {profile.planned_duration_days} days"
            ]
        }

    def generate_checklist_summary(self, validated_items: List[ValidatedRequirement], profile: ApplicantProfile) -> str:
        return (
            f"Personalized document requirements for {profile.destination_country} "
            f"{profile.visa_category} visa for a {profile.employment_status} applicant "
            f"from {profile.nationality}. Based on {len(validated_items)} verified requirement rules."
        )


def get_ai_provider() -> BaseAIProvider:
    if settings.AI_PROVIDER.lower() == "ollama":
        from app.ai.ollama_provider import OllamaProvider
        return OllamaProvider()
    return MockAIProvider()
