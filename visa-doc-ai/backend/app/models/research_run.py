from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, String, Integer, DateTime, Text, JSON
from app.db.session import Base


class ResearchRunModel(Base):
    __tablename__ = "research_runs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    profile_id = Column(String, nullable=True)
    destination_country = Column(String, nullable=False)
    visa_category = Column(String, nullable=False)
    user_question = Column(Text, default="")
    workflow_status = Column(String, default="initializing")
    iteration_count = Column(Integer, default=0)
    search_budget_remaining = Column(Integer, default=5)
    stop_reason = Column(String, nullable=True)
    state_json = Column(Text, nullable=False)  # Serialized ResearchState JSON
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
