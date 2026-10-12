from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.checklist import DocumentChecklist
from app.services.checklist_service import checklist_service

router = APIRouter(prefix="/checklists", tags=["Checklists"])


@router.get("/{checklist_id}", response_model=DocumentChecklist)
def get_checklist(checklist_id: str, db: Session = Depends(get_db)):
    checklist = checklist_service.get_checklist_by_id(checklist_id, db=db)
    if not checklist:
        raise HTTPException(status_code=404, detail="Checklist not found")
    return checklist


@router.get("/run/{run_id}", response_model=DocumentChecklist)
def get_checklist_for_run(run_id: str, db: Session = Depends(get_db)):
    checklist = checklist_service.get_checklist_by_run_id(run_id, db=db)
    if not checklist:
        raise HTTPException(status_code=404, detail=f"Checklist for research run '{run_id}' not found")
    return checklist
