from app.verification.evidence_validator import EvidenceValidator
from app.schemas.requirement import ExtractedEvidence
from app.schemas.source import RetrievedSource, SourceMetadata
from app.schemas.common import ClaimOutcome, SourceTier
from app.schemas.visa_profile import ApplicantProfile


def test_evidence_provenance_verification():
    source = RetrievedSource(
        id="src_1",
        metadata=SourceMetadata(
            url="https://india.diplo.de/checklist",
            domain="india.diplo.de",
            is_official=True,
            tier=SourceTier.OFFICIAL,
        ),
        raw_text="The passport must be valid for at least 3 months beyond the planned departure.",
        is_accessible=True
    )
    
    ev_valid = ExtractedEvidence(
        id="ev_1",
        source_id="src_1",
        source_url="https://india.diplo.de/checklist",
        source_title="Embassy",
        is_official=True,
        exact_quote="valid for at least 3 months beyond the planned departure"
    )
    assert EvidenceValidator.verify_provenance(ev_valid, source) is True
    assert ev_valid.char_offset_start >= 0
    assert ev_valid.char_offset_end > ev_valid.char_offset_start

    ev_fake = ExtractedEvidence(
        id="ev_2",
        source_id="src_1",
        source_url="https://india.diplo.de/checklist",
        source_title="Embassy",
        is_official=True,
        exact_quote="This quote does not exist anywhere in the page."
    )
    assert EvidenceValidator.verify_provenance(ev_fake, source) is False


def test_evaluate_claim_missing_evidence_not_equated_to_unnecessary(sample_profile: ApplicantProfile):
    # Claim with zero evidence must return NOT_ESTABLISHED, NOT "unnecessary"
    outcome, rationale, conf = EvidenceValidator.evaluate_claim(
        claim="Police clearance certificate is not needed",
        evidence_list=[],
        conflicts=[],
        profile=sample_profile
    )
    assert outcome == ClaimOutcome.NOT_ESTABLISHED
    assert "Absence of proof is not proof of absence" in rationale
