from app.schemas.verification import VerificationRequest
from app.schemas.common import ClaimOutcome, RequirementClassification
from app.schemas.visa_profile import ApplicantProfile
from app.schemas.requirement import ExtractedEvidence, ConflictRecord
from app.services.verification_service import VerificationService
from app.verification.evidence_validator import EvidenceValidator


def test_verify_claim_with_official_evidence(sample_profile: ApplicantProfile):
    evidence = [
        ExtractedEvidence(
            id="ev_1",
            source_id="s1",
            source_url="https://india.diplo.de/visa",
            source_title="Embassy",
            is_official=True,
            exact_quote="Passport must be valid for at least 3 months beyond departure date."
        )
    ]
    
    outcome, rationale, conf = EvidenceValidator.evaluate_claim(
        claim="Passport must be valid for 3 months beyond trip",
        evidence_list=evidence,
        conflicts=[],
        profile=sample_profile
    )
    assert outcome == ClaimOutcome.SUPPORTED_BY_OFFICIAL
    assert conf > 0.90
    assert "https://india.diplo.de/visa" in rationale


def test_verify_claim_with_conflicting_information(sample_profile: ApplicantProfile):
    conflict = ConflictRecord(
        requirement_title="Bank Statement Duration",
        issue="Contradictory timeframes (3 vs 6 months)",
        source_a_url="https://india.diplo.de/reqs",
        source_a_claim="3 months statements",
        source_b_url="https://unofficial.com",
        source_b_claim="6 months statements",
        resolution_strategy="Official embassy rules prevail."
    )
    
    outcome, rationale, conf = EvidenceValidator.evaluate_claim(
        claim="Proof of financial means requires bank statements",
        evidence_list=[],
        conflicts=[conflict],
        profile=sample_profile
    )
    assert outcome == ClaimOutcome.CONFLICTING_OFFICIAL
    assert "Discrepancy detected" in rationale


def test_verify_claim_missing_evidence(sample_profile: ApplicantProfile):
    outcome, rationale, conf = EvidenceValidator.evaluate_claim(
        claim="Applicant must provide yellow fever vaccination certificate",
        evidence_list=[],
        conflicts=[],
        profile=sample_profile
    )
    assert outcome == ClaimOutcome.NOT_ESTABLISHED
    assert "Absence of proof is not proof of absence" in rationale
