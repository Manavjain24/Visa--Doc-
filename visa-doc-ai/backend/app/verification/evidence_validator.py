import re
from typing import List, Tuple, Optional
from app.schemas.requirement import ExtractedEvidence, ConflictRecord
from app.schemas.source import RetrievedSource
from app.schemas.common import ClaimOutcome, RequirementClassification
from app.schemas.visa_profile import ApplicantProfile
from app.utils.text_utils import find_quote_offsets


class EvidenceValidator:
    """
    Deterministic validator that assesses evidence provenance and verifies claims
    against retrieved source text.
    """

    @staticmethod
    def verify_provenance(evidence: ExtractedEvidence, source: RetrievedSource) -> bool:
        """Confirms that the excerpt is genuinely traceable to the retrieved source content."""
        if not source.raw_text or not evidence.exact_quote:
            return False
            
        start, end = find_quote_offsets(source.raw_text, evidence.exact_quote)
        if start != -1:
            evidence.char_offset_start = start
            evidence.char_offset_end = end
            return True
            
        return False

    @staticmethod
    def evaluate_claim(
        claim: str,
        evidence_list: List[ExtractedEvidence],
        conflicts: List[ConflictRecord],
        profile: ApplicantProfile
    ) -> Tuple[ClaimOutcome, str, float]:
        """
        Determines the evidentiary outcome for a given document claim.
        Returns: (ClaimOutcome, rationale, confidence_score)
        """
        claim_lower = claim.lower()

        # Check if there is an active conflict
        claim_words = {re.sub(r's$', '', w) for w in re.findall(r'\b[a-zA-Z]{4,}\b', claim_lower) if w not in {"visa", "document", "required", "applicant", "submit"}}
        
        matching_conflicts = []
        for c in conflicts:
            conflict_text = f"{c.requirement_title} {c.issue}".lower()
            c_words = {re.sub(r's$', '', w) for w in re.findall(r'\b[a-zA-Z]{4,}\b', conflict_text)}
            if claim_words & c_words:
                matching_conflicts.append(c)

        if matching_conflicts:
            return (
                ClaimOutcome.CONFLICTING_OFFICIAL,
                f"Discrepancy detected across sources: {matching_conflicts[0].issue}. {matching_conflicts[0].resolution_strategy}",
                0.75
            )

        # Find relevant evidence chunks
        relevant_evidence = []
        for ev in evidence_list:
            ev_text = ev.exact_quote.lower()
            ev_words = {re.sub(r's$', '', w) for w in re.findall(r'\b[a-zA-Z]{4,}\b', ev_text)}
            if claim_words & ev_words:
                relevant_evidence.append(ev)

        if not relevant_evidence:
            return (
                ClaimOutcome.NOT_ESTABLISHED,
                "No reviewed official source currently establishes this document requirement. Note: Absence of proof is not proof of absence.",
                0.3
            )

        official_evidence = [e for e in relevant_evidence if e.is_official]
        if not official_evidence:
            return (
                ClaimOutcome.UNABLE_TO_VERIFY,
                "Mentioned only in secondary or unofficial sources without official embassy confirmation.",
                0.5
            )

        # Check if conditions apply to this applicant
        has_conditions = any(len(e.applicable_conditions) > 0 for e in official_evidence)
        conditional_keywords = ["if employed", "for employees", "if minor", "if student", "when sponsored", "only if"]
        
        found_conditions = []
        for e in official_evidence:
            for kw in conditional_keywords:
                if kw in e.exact_quote.lower():
                    found_conditions.append(kw)

        if has_conditions or found_conditions:
            return (
                ClaimOutcome.SUPPORTED_UNDER_CONDITIONS,
                f"Supported by official evidence under specific conditions: {', '.join(set(found_conditions)) or 'applicable profile conditions'}.",
                0.90
            )

        return (
            ClaimOutcome.SUPPORTED_BY_OFFICIAL,
            f"Explicitly mandated by official immigration authority ({official_evidence[0].source_url}).",
            0.98
        )
