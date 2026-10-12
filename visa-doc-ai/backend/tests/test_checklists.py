from app.schemas.visa_profile import ApplicantProfile
from app.schemas.requirement import ValidatedRequirement, ExtractedEvidence
from app.schemas.common import RequirementClassification, ClaimOutcome
from app.services.research_orchestrator import ResearchOrchestrator, ResearchGraphState


def test_checklist_generation_from_validated_evidence_only(sample_profile: ApplicantProfile):
    orchestrator = ResearchOrchestrator()
    
    val_req = ValidatedRequirement(
        id="val_1",
        candidate_id="cand_1",
        title="Travel Health Insurance",
        description="Mandatory medical policy covering 30,000 EUR",
        classification=RequirementClassification.MANDATORY,
        verification_outcome=ClaimOutcome.SUPPORTED_BY_OFFICIAL,
        confidence_score=0.98,
        conditions=[],
        exceptions=[],
        evidence_ids=["ev_1"],
        source_urls=["https://india.diplo.de/checklist"],
        deterministic_rationale="Explicitly required by official immigration authority."
    )
    
    ev_dict = {
        "id": "ev_1",
        "source_id": "s1",
        "source_url": "https://india.diplo.de/checklist",
        "source_title": "Official German Embassy",
        "is_official": True,
        "exact_quote": "Travel health insurance with minimum coverage of 30,000 EUR.",
        "char_offset_start": 0,
        "char_offset_end": 50,
        "applicable_categories": ["Tourist"],
        "applicable_conditions": []
    }
    
    state: ResearchGraphState = {
        "run_id": "test_run_123",
        "applicant_profile": sample_profile.model_dump(),
        "user_question": "",
        "research_objectives": [],
        "planned_search_tasks": [],
        "executed_queries": [],
        "search_results": [],
        "retrieved_sources": [],
        "extracted_evidence": [ev_dict],
        "candidate_requirements": [],
        "validated_classifications": [val_req.model_dump()],
        "unresolved_questions": ["What is processing time?"],
        "conflicting_evidence": [],
        "iteration_count": 1,
        "max_iterations": 3,
        "search_budget_remaining": 4,
        "max_search_budget": 5,
        "stop_reason": "Complete",
        "errors_and_warnings": [],
        "traces": [],
        "final_checklist": None,
        "workflow_status": "generating_checklist"
    }
    
    res = orchestrator.checklist_generation_node(state)
    checklist = res["final_checklist"]
    
    assert checklist is not None
    assert len(checklist["mandatory_items"]) == 1
    assert checklist["mandatory_items"][0]["title"] == "Travel Health Insurance"
    assert len(checklist["mandatory_items"][0]["citations"]) == 1
    assert checklist["mandatory_items"][0]["citations"][0]["source_url"] == "https://india.diplo.de/checklist"
    assert len(checklist["unresolved_questions"]) == 1
    assert "disclaimer" in checklist
    assert "DOES NOT constitute legal advice" in checklist["disclaimer"]
