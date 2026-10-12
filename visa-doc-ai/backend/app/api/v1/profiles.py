from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.visa_profile import ApplicantProfile, ApplicantProfileResponse
from app.services.profile_service import profile_service

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.post("", response_model=ApplicantProfileResponse)
def create_profile(profile: ApplicantProfile, db: Session = Depends(get_db)):
    model = profile_service.create_profile(profile, db)
    return ApplicantProfileResponse(id=model.id, **profile.model_dump())


@router.get("/{profile_id}", response_model=ApplicantProfile)
def get_profile(profile_id: str, db: Session = Depends(get_db)):
    profile = profile_service.get_profile(profile_id, db)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
