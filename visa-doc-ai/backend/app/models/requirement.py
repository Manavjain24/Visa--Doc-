from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, String, Float, DateTime, Text
from app.db.session import Base


class RequirementModel(Base):
    __tablename__ = "requirements"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    run_id = Column(String, nullable=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    classification = Column(String, nullable=False)  # Mandatory, Conditional, etc.
    verification_outcome = Column(String, nullable=False)
    confidence_score = Column(Float, default=1.0)
    conditions = Column(Text, default="[]")  # JSON
    exceptions = Column(Text, default="[]")  # JSON
    source_urls = Column(Text, default="[]")  # JSON
    rationale = Column(Text, default="")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
