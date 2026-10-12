import re
from typing import List, Optional
from app.schemas.requirement import ConflictRecord, ExtractedEvidence
from app.schemas.source import RetrievedSource


class ConflictDetector:
    """Detects and documents factual discrepancies between retrieved sources."""

    @staticmethod
    def detect_conflicts(evidence_list: List[ExtractedEvidence]) -> List[ConflictRecord]:
        conflicts: List[ConflictRecord] = []
        
        # 1. Bank statement duration conflict detection (3 months vs 6 months)
        bank_evidence = [e for e in evidence_list if "bank" in e.exact_quote.lower() or "statement" in e.exact_quote.lower()]
        has_3_months = [e for e in bank_evidence if re.search(r'\b3\s*(months?|mos?)\b', e.exact_quote, re.I)]
        has_6_months = [e for e in bank_evidence if re.search(r'\b6\s*(months?|mos?)\b', e.exact_quote, re.I)]

        if has_3_months and has_6_months:
            src_a = has_3_months[0]
            src_b = has_6_months[0]
            if src_a.source_url != src_b.source_url:
                strategy = "Precedence rule: If applying through jurisdiction requiring 3 months, 3 months suffices; however, providing 6 months safely satisfies both."
                if src_a.is_official and not src_b.is_official:
                    strategy = f"Official source ({src_a.source_url}) mandates 3 months, superseding unofficial guide."
                elif src_b.is_official and not src_a.is_official:
                    strategy = f"Official source ({src_b.source_url}) mandates 6 months, superseding unofficial guide."

                conflicts.append(
                    ConflictRecord(
                        requirement_title="Proof of Financial Means (Bank Statement Duration)",
                        issue="Discrepancy in required bank statement history (3 months vs 6 months)",
                        source_a_url=src_a.source_url,
                        source_a_claim=src_a.exact_quote[:150],
                        source_b_url=src_b.source_url,
                        source_b_claim=src_b.exact_quote[:150],
                        resolution_strategy=strategy
                    )
                )

        # 2. Passport validity duration conflict (3 months vs 6 months)
        passport_evidence = [e for e in evidence_list if "passport" in e.exact_quote.lower() or "validity" in e.exact_quote.lower()]
        p_3_months = [e for e in passport_evidence if re.search(r'\b3\s*(months?|mos?)\b', e.exact_quote, re.I)]
        p_6_months = [e for e in passport_evidence if re.search(r'\b6\s*(months?|mos?)\b', e.exact_quote, re.I)]

        if p_3_months and p_6_months:
            src_a = p_3_months[0]
            src_b = p_6_months[0]
            if src_a.source_url != src_b.source_url:
                conflicts.append(
                    ConflictRecord(
                        requirement_title="Passport Validity Duration",
                        issue="Sources cite differing required remaining passport validity beyond departure date",
                        source_a_url=src_a.source_url,
                        source_a_claim=src_a.exact_quote[:150],
                        source_b_url=src_b.source_url,
                        source_b_claim=src_b.exact_quote[:150],
                        resolution_strategy="Official Schengen code mandates at least 3 months; consult official embassy portal."
                    )
                )

        return conflicts
