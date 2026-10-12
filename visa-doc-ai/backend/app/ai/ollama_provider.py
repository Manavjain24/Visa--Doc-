import json
from typing import Dict, Any, List
import httpx
from app.core.config import settings
from app.core.logging import logger
from app.ai.base import BaseAIProvider, MockAIProvider
from app.schemas.visa_profile import ApplicantProfile
from app.schemas.requirement import ValidatedRequirement


class OllamaProvider(BaseAIProvider):
    """Ollama local LLM provider with graceful deterministic fallback."""

    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL.rstrip('/')
        self.model = settings.OLLAMA_MODEL
        self._fallback = MockAIProvider()

    def generate_plan(self, profile: ApplicantProfile, user_question: str, gaps: List[str]) -> Dict[str, Any]:
        prompt = (
            f"Generate a research plan for {profile.destination_country} {profile.visa_category} visa.\n"
            f"Applicant is {profile.employment_status} from {profile.nationality}.\n"
            f"User Question: {user_question}\n"
            f"Gaps: {gaps}\n"
            f"Respond in JSON format with 'objectives': list of strings, and 'relevant_conditions': list of strings."
        )
        try:
            with httpx.Client(timeout=10.0) as client:
                res = client.post(
                    f"{self.base_url}/api/generate",
                    json={"model": self.model, "prompt": prompt, "format": "json", "stream": False}
                )
                if res.status_code == 200:
                    data = res.json().get("response", "{}")
                    parsed = json.loads(data)
                    if "objectives" in parsed:
                        return parsed
        except Exception as e:
            logger.info(f"Ollama connection unavailable ({e}); utilizing deterministic planning provider.")

        return self._fallback.generate_plan(profile, user_question, gaps)

    def generate_checklist_summary(self, validated_items: List[ValidatedRequirement], profile: ApplicantProfile) -> str:
        return self._fallback.generate_checklist_summary(validated_items, profile)
