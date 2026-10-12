from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from app.db.session import Base


class VisaProfileModel(Base):
    __tablename__ = "visa_profiles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nationality = Column(String, nullable=False)
    residence_country = Column(String, nullable=False)
    destination_country = Column(String, nullable=False)
    visa_category = Column(String, nullable=False)
    purpose_of_travel = Column(Text, nullable=False)
    planned_duration_days = Column(Integer, default=15)
    employment_status = Column(String, default="Employed")
    financial_sponsor = Column(String, default="Self")
    has_previous_visas = Column(Boolean, default=False)
    special_circumstances = Column(Text, default="[]")  # JSON encoded
    specific_questions = Column(Text, default="[]")  # JSON encoded
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
