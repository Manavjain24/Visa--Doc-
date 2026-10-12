from app.services.profile_service import profile_service
from app.schemas.visa_profile import ApplicantProfile
from app.db.session import SessionLocal
from app.db.init_db import init_db


def test_profile_create_and_retrieve(sample_profile: ApplicantProfile):
    init_db()
    db = SessionLocal()
    try:
        model = profile_service.create_profile(sample_profile, db)
        assert model.id is not None
        assert model.destination_country == "Germany"

        retrieved = profile_service.get_profile(model.id, db)
        assert retrieved is not None
        assert retrieved.nationality == "India"
        assert retrieved.employment_status == "Employed"
    finally:
        db.close()
