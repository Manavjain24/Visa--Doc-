from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.source import SourceModel

router = APIRouter(prefix="/sources", tags=["Sources"])


@router.get("/{source_id}")
def get_source(source_id: str, db: Session = Depends(get_db)):
    source = db.query(SourceModel).filter(SourceModel.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return {
        "id": source.id,
        "run_id": source.run_id,
        "url": source.url,
        "domain": source.domain,
        "title": source.title,
        "is_official": source.is_official,
        "tier": source.tier,
        "raw_text": source.raw_text,
        "retrieved_at": source.retrieved_at
    }
