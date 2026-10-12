from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.verification import VerificationRequest, VerificationResult
from app.services.verification_service import verification_service

router = APIRouter(prefix="/verification", tags=["Verification"])


@router.post("/verify-claim", response_model=VerificationResult)
def verify_claim(request: VerificationRequest, db: Session = Depends(get_db)):
    return verification_service.verify_claim(request, db=db)
