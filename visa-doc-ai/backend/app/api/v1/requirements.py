from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.requirement import ValidatedRequirement
from app.services.requirement_service import requirement_service

router = APIRouter(prefix="/requirements", tags=["Requirements"])


@router.get("/run/{run_id}", response_model=List[ValidatedRequirement])
def get_requirements_for_run(run_id: str, db: Session = Depends(get_db)):
    return requirement_service.get_requirements_by_run(run_id, db=db)
