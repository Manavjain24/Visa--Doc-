from typing import Optional, List
from sqlalchemy.orm import Session
from app.schemas.verification import VerificationRequest, VerificationResult
from app.schemas.common import ClaimOutcome, RequirementClassification
from app.schemas.requirement import ExtractedEvidence, CandidateRequirement
from app.verification.evidence_validator import EvidenceValidator
from app.verification.conflict_detector import ConflictDetector
from app.verification.classifier import DeterministicClassifier
from app.models.research_run import ResearchRunModel
from app.schemas.research import ResearchState


class VerificationService:
    """Service dedicated to testing document requirement claims against verified evidence."""

    def verify_claim(self, request: VerificationRequest, db: Optional[Session] = None) -> VerificationResult:
        claim = request.claim_statement.strip()
        profile = request.applicant_profile

        # Gather relevant evidence from existing research runs if db available
        evidence_pool: List[ExtractedEvidence] = []
        if db:
            runs = db.query(ResearchRunModel).filter(
                ResearchRunModel.destination_country == profile.destination_country
            ).all()
            for r in runs:
                state = ResearchState.model_validate_json(r.state_json)
                evidence_pool.extend(state.extracted_evidence)

        conflicts = ConflictDetector.detect_conflicts(evidence_pool)
        outcome, rationale, conf_score = EvidenceValidator.evaluate_claim(claim, evidence_pool, conflicts, profile)

        # Classify candidate claim deterministically
        cand = CandidateRequirement(
            id="adhoc_claim",
            title=claim[:60],
            description=claim,
            proposed_classification=RequirementClassification.MANDATORY,
            supporting_evidence_ids=[e.id for e in evidence_pool]
        )
        val = DeterministicClassifier.classify_requirement(cand, evidence_pool, profile)

        sources = list({e.source_url for e in evidence_pool if e.is_official})

        return VerificationResult(
            claim_statement=claim,
            outcome=outcome,
            classification=val.classification,
            is_verified=(outcome == ClaimOutcome.SUPPORTED_BY_OFFICIAL or outcome == ClaimOutcome.SUPPORTED_UNDER_CONDITIONS),
            rationale=rationale,
            supporting_evidence=evidence_pool[:3],
            conflicting_evidence=conflicts,
            sources_consulted=sources[:5]
        )


verification_service = VerificationService()
