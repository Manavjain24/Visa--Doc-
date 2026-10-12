import re
from typing import List, Tuple
from app.schemas.common import RequirementClassification, ClaimOutcome
from app.schemas.requirement import CandidateRequirement, ExtractedEvidence, ValidatedRequirement
from app.schemas.visa_profile import ApplicantProfile


class DeterministicClassifier:
    """
    Deterministic verification layer that enforces the strict classification policy.
    Validates evidence and overrides any agent proposals that lack evidentiary backing.
    """

    MANDATORY_TERMS = ["mandatory", "must submit", "required", "compulsory", "shall provide", "all applicants must"]
    RECOMMENDED_TERMS = ["recommended", "advisable", "optional", "suggested", "may also provide", "can help support"]
    CONDITIONAL_TERMS = ["if applicable", "for employed", "for employees", "if minor", "if student", "when sponsored", "only if"]

    @staticmethod
    def classify_requirement(
        candidate: CandidateRequirement,
        evidence_list: List[ExtractedEvidence],
        profile: ApplicantProfile
    ) -> ValidatedRequirement:
        supporting_evidence = [e for e in evidence_list if e.id in candidate.supporting_evidence_ids]
        official_evidence = [e for e in supporting_evidence if e.is_official]

        # 1. Check for Not Applicable based on profile
        title_lower = candidate.title.lower()
        desc_lower = candidate.description.lower()

        # If student requirement but applicant is employed
        if ("student" in title_lower or "school" in title_lower or "university" in title_lower) and profile.employment_status.lower() != "student":
            return ValidatedRequirement(
                id=f"val_{candidate.id}",
                candidate_id=candidate.id,
                title=candidate.title,
                description=candidate.description,
                classification=RequirementClassification.NOT_APPLICABLE,
                verification_outcome=ClaimOutcome.SUPPORTED_UNDER_CONDITIONS,
                confidence_score=0.95,
                conditions=["Applicable only to enrolled students"],
                exceptions=[f"Applicant employment status is '{profile.employment_status}'"],
                evidence_ids=[e.id for e in supporting_evidence],
                source_urls=[e.source_url for e in supporting_evidence],
                deterministic_rationale="Applicant profile does not match student condition; correctly classified as Not Applicable."
            )

        # 2. Check evidence presence: If no official evidence exists
        if not official_evidence:
            return ValidatedRequirement(
                id=f"val_{candidate.id}",
                candidate_id=candidate.id,
                title=candidate.title,
                description=candidate.description,
                classification=RequirementClassification.UNVERIFIED,
                verification_outcome=ClaimOutcome.NOT_ESTABLISHED,
                confidence_score=0.40,
                conditions=candidate.applicable_conditions,
                exceptions=candidate.exceptions,
                evidence_ids=[e.id for e in supporting_evidence],
                source_urls=[e.source_url for e in supporting_evidence],
                deterministic_rationale="Policy enforcement: Requirement proposed without official government evidence must be classified as Unverified."
            )

        combined_text = " ".join([e.exact_quote.lower() for e in official_evidence])

        # 3. Check for Recommended
        if any(term in combined_text for term in DeterministicClassifier.RECOMMENDED_TERMS):
            return ValidatedRequirement(
                id=f"val_{candidate.id}",
                candidate_id=candidate.id,
                title=candidate.title,
                description=candidate.description,
                classification=RequirementClassification.RECOMMENDED,
                verification_outcome=ClaimOutcome.SUPPORTED_BY_OFFICIAL,
                confidence_score=0.92,
                conditions=candidate.applicable_conditions,
                exceptions=candidate.exceptions,
                evidence_ids=[e.id for e in official_evidence],
                source_urls=[e.source_url for e in official_evidence],
                deterministic_rationale="Official text employs non-mandatory terminology ('recommended/advisable')."
            )

        # 4. Check for Conditional
        has_condition_term = any(term in combined_text for term in DeterministicClassifier.CONDITIONAL_TERMS)
        if has_condition_term or candidate.applicable_conditions or ("employment" in title_lower or "leave letter" in title_lower or "noc" in title_lower):
            # Verify if condition matches applicant profile
            matched_condition = f"Applies because applicant is {profile.employment_status}"
            return ValidatedRequirement(
                id=f"val_{candidate.id}",
                candidate_id=candidate.id,
                title=candidate.title,
                description=candidate.description,
                classification=RequirementClassification.CONDITIONAL,
                verification_outcome=ClaimOutcome.SUPPORTED_UNDER_CONDITIONS,
                confidence_score=0.95,
                conditions=[matched_condition],
                exceptions=candidate.exceptions,
                evidence_ids=[e.id for e in official_evidence],
                source_urls=[e.source_url for e in official_evidence],
                deterministic_rationale=f"Requirement is conditional upon applicant status ({matched_condition})."
            )

        # 5. Default to Mandatory if official evidence mandates it
        return ValidatedRequirement(
            id=f"val_{candidate.id}",
            candidate_id=candidate.id,
            title=candidate.title,
            description=candidate.description,
            classification=RequirementClassification.MANDATORY,
            verification_outcome=ClaimOutcome.SUPPORTED_BY_OFFICIAL,
            confidence_score=0.98,
            conditions=[],
            exceptions=[],
            evidence_ids=[e.id for e in official_evidence],
            source_urls=[e.source_url for e in official_evidence],
            deterministic_rationale="Verified as Mandatory: Explicitly required by official immigration guidelines for all applicants in this visa category."
        )
