from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from app.db.session import Base


class EvidenceModel(Base):
    __tablename__ = "evidence"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id = Column(String, nullable=False, index=True)
    source_url = Column(String, nullable=False)
    source_title = Column(String, default="")
    is_official = Column(Boolean, default=False)
    exact_quote = Column(Text, nullable=False)
    char_offset_start = Column(Integer, default=0)
    char_offset_end = Column(Integer, default=0)
    applicable_categories = Column(Text, default="[]")  # JSON
    extracted_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
