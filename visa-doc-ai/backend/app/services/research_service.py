import json
import uuid
from typing import Optional, List
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logging import logger
from app.schemas.visa_profile import ApplicantProfile
from app.schemas.research import ResearchState, ResearchRunSummary
from app.schemas.common import ResearchStatus
from app.models.research_run import ResearchRunModel
from app.models.checklist import ChecklistModel
from app.services.research_orchestrator import ResearchOrchestrator
from app.search.serpapi_provider import SerpApiProvider
from app.ingestion.page_fetcher import PageFetcher


class ResearchService:
    """Service managing research execution, persistence, and state tracking."""

    def __init__(self, orchestrator: Optional[ResearchOrchestrator] = None):
        self.orchestrator = orchestrator or ResearchOrchestrator()

    def start_research(
        self,
        profile: ApplicantProfile,
        user_question: str = "",
        max_iterations: Optional[int] = None,
        max_search_budget: Optional[int] = None,
        db: Optional[Session] = None
    ) -> ResearchState:
        run_id = str(uuid.uuid4())
        max_iter = max_iterations or settings.RESEARCH_MAX_ITERATIONS
        max_budget = max_search_budget or settings.RESEARCH_MAX_SEARCH_BUDGET

        initial_state = ResearchState(
            run_id=run_id,
            applicant_profile=profile,
            user_question=user_question or "",
            max_iterations=max_iter,
            max_search_budget=max_budget,
            search_budget_remaining=max_budget,
            iteration_count=0,
            workflow_status=ResearchStatus.INITIALIZING
        )

        logger.info(f"Starting agentic research run {run_id} for {profile.destination_country} {profile.visa_category}")
        final_state = self.orchestrator.run(initial_state)

        # Persist to DB if session provided
        if db:
            run_record = ResearchRunModel(
                id=run_id,
                destination_country=profile.destination_country,
                visa_category=profile.visa_category,
                user_question=user_question,
                workflow_status=final_state.workflow_status.value,
                iteration_count=final_state.iteration_count,
                search_budget_remaining=final_state.search_budget_remaining,
                stop_reason=final_state.stop_reason,
                state_json=final_state.model_dump_json()
            )
            db.add(run_record)

            if final_state.final_checklist:
                checklist_record = ChecklistModel(
                    id=final_state.final_checklist.id,
                    run_id=run_id,
                    destination_country=profile.destination_country,
                    visa_category=profile.visa_category,
                    checklist_json=final_state.final_checklist.model_dump_json()
                )
                db.add(checklist_record)

            db.commit()

        return final_state

    def get_research_state(self, run_id: str, db: Optional[Session] = None) -> Optional[ResearchState]:
        if not db:
            return None
        record = db.query(ResearchRunModel).filter(ResearchRunModel.id == run_id).first()
        if not record:
            return None
        return ResearchState.model_validate_json(record.state_json)

    def list_runs(self, db: Optional[Session] = None) -> List[ResearchRunSummary]:
        if not db:
            return []
        records = db.query(ResearchRunModel).order_by(ResearchRunModel.created_at.desc()).limit(20).all()
        summaries = []
        for r in records:
            state = ResearchState.model_validate_json(r.state_json)
            summaries.append(
                ResearchRunSummary(
                    run_id=r.id,
                    workflow_status=state.workflow_status,
                    iteration_count=state.iteration_count,
                    search_budget_remaining=state.search_budget_remaining,
                    objectives_count=len(state.research_objectives),
                    sources_count=len(state.retrieved_sources),
                    evidence_count=len(state.extracted_evidence),
                    validated_requirements_count=len(state.validated_classifications),
                    unresolved_questions_count=len(state.unresolved_questions),
                    stop_reason=state.stop_reason,
                    has_checklist=state.final_checklist is not None,
                    created_at=r.created_at,
                    updated_at=r.updated_at
                )
            )
        return summaries


research_service = ResearchService()
