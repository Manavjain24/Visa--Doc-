import json
from typing import Optional, List
from sqlalchemy.orm import Session
from app.schemas.visa_profile import ApplicantProfile, ApplicantProfileCreate
from app.models.visa_profile import VisaProfileModel


class ProfileService:
    """Service for storing and retrieving applicant profiles."""

    def create_profile(self, profile: ApplicantProfile, db: Session) -> VisaProfileModel:
        model = VisaProfileModel(
            nationality=profile.nationality,
            residence_country=profile.residence_country,
            destination_country=profile.destination_country,
            visa_category=profile.visa_category,
            purpose_of_travel=profile.purpose_of_travel,
            planned_duration_days=profile.planned_duration_days,
            employment_status=profile.employment_status,
            financial_sponsor=profile.financial_sponsor,
            has_previous_visas=profile.has_previous_visas,
            special_circumstances=json.dumps(profile.special_circumstances),
            specific_questions=json.dumps(profile.specific_questions),
        )
        db.add(model)
        db.commit()
        db.refresh(model)
        return model

    def get_profile(self, profile_id: str, db: Session) -> Optional[ApplicantProfile]:
        model = db.query(VisaProfileModel).filter(VisaProfileModel.id == profile_id).first()
        if not model:
            return None
        return ApplicantProfile(
            nationality=model.nationality,
            residence_country=model.residence_country,
            destination_country=model.destination_country,
            visa_category=model.visa_category,
            purpose_of_travel=model.purpose_of_travel,
            planned_duration_days=model.planned_duration_days,
            employment_status=model.employment_status,
            financial_sponsor=model.financial_sponsor,
            has_previous_visas=model.has_previous_visas,
            special_circumstances=json.loads(model.special_circumstances or "[]"),
            specific_questions=json.loads(model.specific_questions or "[]"),
        )


profile_service = ProfileService()
