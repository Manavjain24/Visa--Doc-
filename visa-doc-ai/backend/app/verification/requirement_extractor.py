import re
import uuid
from typing import List, Tuple
from app.schemas.source import RetrievedSource
from app.schemas.requirement import ExtractedEvidence, CandidateRequirement
from app.schemas.common import RequirementClassification
from app.schemas.visa_profile import ApplicantProfile
from app.utils.text_utils import find_quote_offsets

KEY_PATTERNS = [
    {
        "title": "Valid Passport / Travel Document",
        "keywords": [r"valid passport", r"travel document", r"blank visa pages", r"passport validity"],
        "classification": RequirementClassification.MANDATORY,
        "description": "Original national passport valid beyond travel duration with required blank visa pages."
    },
    {
        "title": "Biometric Photographs",
        "keywords": [r"biometric photograph", r"passport photos", r"photographs?", r"photo specifications"],
        "classification": RequirementClassification.MANDATORY,
        "description": "Recent passport-sized biometric photographs matching standard dimensions."
    },
    {
        "title": "Travel Health Insurance",
        "keywords": [r"travel health insurance", r"medical insurance", r"minimum coverage", r"30,000\s*eur"],
        "classification": RequirementClassification.MANDATORY,
        "description": "Travel medical insurance policy covering emergency care, hospitalization, and repatriation."
    },
    {
        "title": "Proof of Financial Means (Bank Statements)",
        "keywords": [r"bank statements?", r"financial means", r"sufficient funds", r"financial sufficiency"],
        "classification": RequirementClassification.MANDATORY,
        "description": "Certified bank account statements showing adequate financial funds for the entire stay."
    },
    {
        "title": "Proof of Accommodation",
        "keywords": [r"hotel reservation", r"accommodation", r"proof of stay", r"invitation letter", r"verpflichtungserklärung"],
        "classification": RequirementClassification.MANDATORY,
        "description": "Confirmed lodging reservations, hotel bookings, or formal letter of host sponsorship."
    },
    {
        "title": "Flight Itinerary / Travel Reservations",
        "keywords": [r"flight booking", r"flight itinerary", r"round-trip flight", r"travel reservation"],
        "classification": RequirementClassification.MANDATORY,
        "description": "Confirmed round-trip flight booking or detailed travel itinerary with dates."
    },
    {
        "title": "Employment Proof & Approved Leave Letter",
        "keywords": [r"leave letter", r"no-objection certificate", r"noc", r"employment proof", r"salary slips"],
        "classification": RequirementClassification.CONDITIONAL,
        "description": "Approved leave letter on company letterhead and recent payslips for employed applicants."
    },
    {
        "title": "Enrollment Certificate (Student)",
        "keywords": [r"student enrollment", r"school certificate", r"university letter"],
        "classification": RequirementClassification.CONDITIONAL,
        "description": "Proof of current student enrollment from university or academic institution."
    }
]


class RequirementExtractor:
    """Extracts candidate requirements and evidence excerpts from retrieved source text."""

    @staticmethod
    def extract_from_source(
        source: RetrievedSource,
        profile: ApplicantProfile
    ) -> Tuple[List[ExtractedEvidence], List[CandidateRequirement]]:
        if not source.raw_text or not source.is_accessible:
            return [], []

        evidence_list: List[ExtractedEvidence] = []
        candidate_list: List[CandidateRequirement] = []
        raw = source.raw_text

        for pattern in KEY_PATTERNS:
            matched_sentences: List[str] = []
            # Split raw text into sentences or paragraphs
            blocks = re.split(r'\n{2,}|\.\s+', raw)
            for block in blocks:
                clean_block = block.strip()
                if not clean_block or len(clean_block) < 20:
                    continue
                for kw in pattern["keywords"]:
                    if re.search(kw, clean_block, re.IGNORECASE):
                        matched_sentences.append(clean_block)
                        break

            if matched_sentences:
                quote = matched_sentences[0]
                # Keep quote concise
                if len(quote) > 300:
                    quote = quote[:300] + "..."

                start_offset, end_offset = find_quote_offsets(raw, quote.rstrip("."))
                if start_offset == -1:
                    start_offset, end_offset = 0, len(quote)

                ev_id = f"ev_{uuid.uuid4().hex[:8]}"
                cand_id = f"cand_{uuid.uuid4().hex[:8]}"

                conditions = []
                if "employed" in quote.lower() or pattern["classification"] == RequirementClassification.CONDITIONAL:
                    conditions.append(f"Applicable for {profile.employment_status} status")

                evidence_obj = ExtractedEvidence(
                    id=ev_id,
                    source_id=source.id,
                    source_url=source.metadata.url,
                    source_title=source.metadata.title,
                    is_official=source.metadata.is_official,
                    exact_quote=quote,
                    char_offset_start=start_offset,
                    char_offset_end=end_offset,
                    applicable_categories=[profile.visa_category],
                    applicable_conditions=conditions
                )
                evidence_list.append(evidence_obj)

                candidate_obj = CandidateRequirement(
                    id=cand_id,
                    title=pattern["title"],
                    description=pattern["description"],
                    proposed_classification=pattern["classification"],
                    applicable_conditions=conditions,
                    exceptions=[],
                    supporting_evidence_ids=[ev_id]
                )
                candidate_list.append(candidate_obj)

        return evidence_list, candidate_list
