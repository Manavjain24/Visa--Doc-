from typing import List, Optional
from sqlalchemy.orm import Session
from app.schemas.requirement import ValidatedRequirement
from app.models.research_run import ResearchRunModel
from app.schemas.research import ResearchState


class RequirementService:
    """Service for querying requirements discovered during research runs."""

    def get_requirements_by_run(self, run_id: str, db: Session) -> List[ValidatedRequirement]:
        run = db.query(ResearchRunModel).filter(ResearchRunModel.id == run_id).first()
        if not run:
            return []
        state = ResearchState.model_validate_json(run.state_json)
        return state.validated_classifications


requirement_service = RequirementService()
