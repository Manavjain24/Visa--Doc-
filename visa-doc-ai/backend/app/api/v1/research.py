from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.research import ResearchRunCreate, ResearchState, ResearchRunSummary
from app.services.research_service import research_service

router = APIRouter(prefix="/research", tags=["Research"])


@router.post("/start", response_model=ResearchState)
def start_research_run(payload: ResearchRunCreate, db: Session = Depends(get_db)):
    try:
        final_state = research_service.start_research(
            profile=payload.applicant_profile,
            user_question=payload.user_question or "",
            max_iterations=payload.max_iterations,
            max_search_budget=payload.max_search_budget,
            db=db
        )
        return final_state
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research orchestrator failed: {str(e)}")


@router.get("/{run_id}", response_model=ResearchState)
def get_research_run(run_id: str, db: Session = Depends(get_db)):
    state = research_service.get_research_state(run_id, db=db)
    if not state:
        raise HTTPException(status_code=404, detail=f"Research run '{run_id}' not found")
    return state


@router.get("", response_model=List[ResearchRunSummary])
def list_research_runs(db: Session = Depends(get_db)):
    return research_service.list_runs(db=db)
