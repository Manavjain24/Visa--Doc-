from typing import List, Optional
from app.schemas.visa_profile import ApplicantProfile
from app.schemas.search import SearchTask


# Known official domain hints by country
COUNTRY_OFFICIAL_DOMAIN_HINTS = {
    "germany": ["germany.info", "diplo.de", "auswaertiges-amt.de"],
    "united states": ["state.gov", "travel.state.gov", "uscis.gov"],
    "usa": ["state.gov", "travel.state.gov", "uscis.gov"],
    "uk": ["gov.uk"],
    "united kingdom": ["gov.uk"],
    "canada": ["canada.ca", "cic.gc.ca"],
    "france": ["france-visas.gouv.fr", "diplomatie.gouv.fr"],
    "italy": ["esteri.it"],
    "spain": ["exteriores.gob.es"],
    "switzerland": ["sem.admin.ch"],
    "netherlands": ["netherlandsworldwide.nl", "ind.nl"],
    "australia": ["homeaffairs.gov.au"],
    "japan": ["mofa.go.jp"],
    "singapore": ["ica.gov.sg"],
}


class QueryBuilder:
    """Constructs targeted, high-precision search queries for visa requirements."""

    @staticmethod
    def build_initial_tasks(profile: ApplicantProfile, user_question: str = "") -> List[SearchTask]:
        dest = profile.destination_country.strip()
        cat = profile.visa_category.strip()
        nat = profile.nationality.strip()
        res = profile.residence_country.strip()

        domain_hints = COUNTRY_OFFICIAL_DOMAIN_HINTS.get(dest.lower(), [])
        site_filter = f"site:{domain_hints[0]}" if domain_hints else "official government embassy"

        tasks: List[SearchTask] = []

        # 1. Primary official checklist query
        tasks.append(
            SearchTask(
                query=f"{dest} {cat} visa required documents checklist {site_filter}",
                objective=f"Retrieve official mandatory document checklist for {dest} {cat} visa",
                priority=1,
                target_domains=domain_hints,
                rationale="Identify baseline official required documents and eligibility criteria."
            )
        )

        # 2. Jurisdiction & Applicant conditions query
        applicant_condition = f"employed applicant" if profile.employment_status == "Employed" else profile.employment_status
        tasks.append(
            SearchTask(
                query=f"{dest} embassy in {res} {cat} visa application documents {applicant_condition} {nat} citizen",
                objective=f"Verify jurisdiction-specific requirements for {nat} citizens applying from {res}",
                priority=2,
                target_domains=domain_hints,
                rationale="Confirm jurisdictional rules and employment-specific requirements."
            )
        )

        # 3. User question specific query if provided
        if user_question and user_question.strip():
            clean_q = user_question.strip()
            tasks.append(
                SearchTask(
                    query=f"{dest} {cat} visa {clean_q} official requirement",
                    objective=f"Address specific user question: '{clean_q}'",
                    priority=1,
                    target_domains=domain_hints,
                    rationale="Directly answer user's specific document query."
                )
            )

        return tasks

    @staticmethod
    def build_gap_queries(profile: ApplicantProfile, unresolved_questions: List[str]) -> List[SearchTask]:
        """Constructs targeted queries specifically to answer remaining evidence gaps."""
        dest = profile.destination_country.strip()
        cat = profile.visa_category.strip()
        domain_hints = COUNTRY_OFFICIAL_DOMAIN_HINTS.get(dest.lower(), [])

        gap_tasks: List[SearchTask] = []
        for i, gap in enumerate(unresolved_questions, start=1):
            gap_clean = gap.strip().rstrip("?")
            gap_tasks.append(
                SearchTask(
                    query=f"{dest} {cat} visa {gap_clean} official immigration requirement",
                    objective=f"Resolve evidence gap: {gap}",
                    priority=1,
                    target_domains=domain_hints,
                    rationale=f"Targeted search to obtain missing proof for: {gap}"
                )
            )
        return gap_tasks
