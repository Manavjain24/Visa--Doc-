from app.verification.classifier import DeterministicClassifier
from app.schemas.requirement import CandidateRequirement, ExtractedEvidence
from app.schemas.common import RequirementClassification
from app.schemas.visa_profile import ApplicantProfile


def test_classifier_enforces_mandatory_with_official_evidence(sample_profile: ApplicantProfile):
    evidence = ExtractedEvidence(
        id="ev_1",
        source_id="src_1",
        source_url="https://india.diplo.de/checklist",
        source_title="Embassy Checklist",
        is_official=True,
        exact_quote="All applicants must submit travel health insurance with min coverage of 30,000 EUR."
    )
    candidate = CandidateRequirement(
        id="c_1",
        title="Travel Health Insurance",
        description="Mandatory medical policy",
        proposed_classification=RequirementClassification.MANDATORY,
        supporting_evidence_ids=["ev_1"]
    )
    
    validated = DeterministicClassifier.classify_requirement(candidate, [evidence], sample_profile)
    assert validated.classification == RequirementClassification.MANDATORY
    assert validated.confidence_score >= 0.95
    assert len(validated.source_urls) == 1


def test_classifier_overrides_to_unverified_if_evidence_is_unofficial(sample_profile: ApplicantProfile):
    evidence = ExtractedEvidence(
        id="ev_2",
        source_id="src_2",
        source_url="https://travel-blog.com/tips",
        source_title="Travel Blog",
        is_official=False,
        exact_quote="You must bring your birth certificate."
    )
    candidate = CandidateRequirement(
        id="c_2",
        title="Birth Certificate",
        description="Birth certificate requirement",
        proposed_classification=RequirementClassification.MANDATORY,
        supporting_evidence_ids=["ev_2"]
    )
    
    # Even if candidate was proposed as MANDATORY, deterministic policy MUST classify as UNVERIFIED
    validated = DeterministicClassifier.classify_requirement(candidate, [evidence], sample_profile)
    assert validated.classification == RequirementClassification.UNVERIFIED
    assert "without official government evidence" in validated.deterministic_rationale


def test_classifier_not_applicable_for_non_matching_profile(sample_profile: ApplicantProfile):
    # sample_profile has employment_status="Employed"
    evidence = ExtractedEvidence(
        id="ev_3",
        source_id="src_3",
        source_url="https://india.diplo.de/checklist",
        source_title="Embassy Checklist",
        is_official=True,
        exact_quote="Students must submit university enrollment letter."
    )
    candidate = CandidateRequirement(
        id="c_3",
        title="University Student Enrollment Letter",
        description="Enrollment verification",
        proposed_classification=RequirementClassification.MANDATORY,
        supporting_evidence_ids=["ev_3"]
    )
    
    validated = DeterministicClassifier.classify_requirement(candidate, [evidence], sample_profile)
    assert validated.classification == RequirementClassification.NOT_APPLICABLE
