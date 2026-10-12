from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, String, DateTime, Text
from app.db.session import Base


class ChecklistModel(Base):
    __tablename__ = "checklists"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    run_id = Column(String, nullable=False, index=True)
    destination_country = Column(String, nullable=False)
    visa_category = Column(String, nullable=False)
    checklist_json = Column(Text, nullable=False)  # Full DocumentChecklist JSON
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
