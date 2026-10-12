from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from app.db.session import Base


class SourceModel(Base):
    __tablename__ = "sources"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    run_id = Column(String, nullable=True, index=True)
    url = Column(String, nullable=False, index=True)
    domain = Column(String, nullable=False)
    title = Column(String, default="")
    is_official = Column(Boolean, default=False)
    tier = Column(String, default="general")
    http_status = Column(Integer, default=200)
    raw_text = Column(Text, default="")
    content_hash = Column(String, default="")
    retrieved_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
