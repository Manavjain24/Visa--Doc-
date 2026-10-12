import json
from typing import Optional
from sqlalchemy.orm import Session
from app.schemas.checklist import DocumentChecklist
from app.models.checklist import ChecklistModel


class ChecklistService:
    """Service to retrieve generated checklists."""

    def get_checklist_by_id(self, checklist_id: str, db: Session) -> Optional[DocumentChecklist]:
        record = db.query(ChecklistModel).filter(ChecklistModel.id == checklist_id).first()
        if not record:
            return None
        return DocumentChecklist.model_validate_json(record.checklist_json)

    def get_checklist_by_run_id(self, run_id: str, db: Session) -> Optional[DocumentChecklist]:
        record = db.query(ChecklistModel).filter(ChecklistModel.run_id == run_id).first()
        if not record:
            return None
        return DocumentChecklist.model_validate_json(record.checklist_json)


checklist_service = ChecklistService()
