import uuid
from datetime import datetime, timezone
from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, START, END

from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import SerpApiException, SearchBudgetExhaustedException
from app.schemas.common import ResearchStatus, RequirementClassification, ClaimOutcome, current_utc_time
from app.schemas.visa_profile import ApplicantProfile
from app.schemas.search import SearchTask, SearchResultItem
from app.schemas.source import RetrievedSource, SourceMetadata
from app.schemas.requirement import (
    ExtractedEvidence,
    CandidateRequirement,
    ValidatedRequirement,
    ConflictRecord
)
from app.schemas.checklist import ChecklistItem, ChecklistCitation, DocumentChecklist
from app.schemas.research import ResearchTraceEntry, ResearchState

from app.search.base import BaseSearchProvider
from app.search.serpapi_provider import SerpApiProvider
from app.search.query_builder import QueryBuilder
from app.ingestion.page_fetcher import PageFetcher
from app.verification.source_ranker import SourceRanker
from app.verification.evidence_validator import EvidenceValidator
from app.verification.conflict_detector import ConflictDetector
from app.verification.classifier import DeterministicClassifier
from app.verification.requirement_extractor import RequirementExtractor
from app.ai.base import get_ai_provider


class ResearchGraphState(TypedDict):
    run_id: str
    applicant_profile: Dict[str, Any]
    user_question: str
    research_objectives: List[str]
    planned_search_tasks: List[Dict[str, Any]]
    executed_queries: List[str]
    search_results: List[Dict[str, Any]]
    retrieved_sources: List[Dict[str, Any]]
    extracted_evidence: List[Dict[str, Any]]
    candidate_requirements: List[Dict[str, Any]]
    validated_classifications: List[Dict[str, Any]]
    unresolved_questions: List[str]
    conflicting_evidence: List[Dict[str, Any]]
    iteration_count: int
    max_iterations: int
    search_budget_remaining: int
    max_search_budget: int
    stop_reason: Optional[str]
    should_refine: bool
    errors_and_warnings: List[str]
    traces: List[Dict[str, Any]]
    final_checklist: Optional[Dict[str, Any]]
    workflow_status: str


def _create_trace(
    stage: str,
    agent_name: str,
    action: str,
    summary: str,
    details: Dict[str, Any] = None,
    evidence_ids: List[str] = None,
    source_urls: List[str] = None
) -> Dict[str, Any]:
    trace = ResearchTraceEntry(
        id=f"tr_{uuid.uuid4().hex[:8]}",
        timestamp=current_utc_time(),
        stage=stage,
        agent_name=agent_name,
        action=action,
        summary=summary,
        details=details or {},
        evidence_ids=evidence_ids or [],
        source_urls=source_urls or []
    )
    return trace.model_dump()


class ResearchOrchestrator:
    """
    Coordinates multi-stage bounded agentic research using LangGraph.
    Enforces strict execution limits, traceable evidence extraction,
    and deterministic verification policies.
    """

    def __init__(self, search_provider: Optional[BaseSearchProvider] = None, page_fetcher: Optional[PageFetcher] = None):
        self.search_provider = search_provider or SerpApiProvider()
        self.page_fetcher = page_fetcher or PageFetcher()
        self.ai_provider = get_ai_provider()
        self.app = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(ResearchGraphState)

        workflow.add_node("research_planner", self.research_planner_node)
        workflow.add_node("search_agent", self.search_node)
        workflow.add_node("evidence_extractor", self.evidence_extraction_node)
        workflow.add_node("requirement_verifier", self.requirement_verification_node)
        workflow.add_node("completeness_evaluator", self.completeness_evaluation_node)
        workflow.add_node("checklist_generator", self.checklist_generation_node)

        workflow.add_edge(START, "research_planner")
        workflow.add_edge("research_planner", "search_agent")
        workflow.add_edge("search_agent", "evidence_extractor")
        workflow.add_edge("evidence_extractor", "requirement_verifier")
        workflow.add_edge("requirement_verifier", "completeness_evaluator")

        workflow.add_conditional_edges(
            "completeness_evaluator",
            self.completeness_router,
            {
                "research_planner": "research_planner",
                "checklist_generator": "checklist_generator"
            }
        )

        workflow.add_edge("checklist_generator", END)
        return workflow.compile()

    # --- NODE 1: RESEARCH PLANNER AGENT ---
    def research_planner_node(self, state: ResearchGraphState) -> Dict[str, Any]:
        iteration = state.get("iteration_count", 0)
        profile_data = state["applicant_profile"]
        profile = ApplicantProfile(**profile_data)
        user_q = state.get("user_question", "")
        unresolved = state.get("unresolved_questions", [])
        executed = set(state.get("executed_queries", []))

        planned_tasks = []

        if iteration == 0:
            # Initial comprehensive plan
            ai_plan = self.ai_provider.generate_plan(profile, user_q, unresolved)
            objectives = ai_plan.get("objectives", [])
            initial_tasks = QueryBuilder.build_initial_tasks(profile, user_q)
            for t in initial_tasks:
                if t.query not in executed:
                    planned_tasks.append(t.model_dump())

            trace = _create_trace(
                stage="Planning",
                agent_name="Research Planner Agent",
                action="Initialize Research Plan",
                summary=f"Formulated {len(objectives)} research objectives and {len(planned_tasks)} initial targeted search tasks.",
                details={"objectives_count": len(objectives), "tasks_count": len(planned_tasks), "iteration": iteration}
            )
            return {
                "research_objectives": objectives,
                "planned_search_tasks": planned_tasks,
                "workflow_status": ResearchStatus.PLANNING.value,
                "traces": state.get("traces", []) + [trace]
            }
        else:
            # Refinement / Gap-focused plan
            gap_tasks = QueryBuilder.build_gap_queries(profile, unresolved)
            for t in gap_tasks:
                if t.query not in executed:
                    planned_tasks.append(t.model_dump())

            trace = _create_trace(
                stage="Refinement",
                agent_name="Research Planner Agent",
                action="Plan Gap Searches",
                summary=f"Iteration {iteration}: Identified {len(unresolved)} evidence gaps. Scheduled {len(planned_tasks)} new targeted search queries.",
                details={"unresolved_questions": unresolved, "new_queries_count": len(planned_tasks), "iteration": iteration}
            )
            return {
                "planned_search_tasks": planned_tasks,
                "workflow_status": ResearchStatus.PLANNING.value,
                "traces": state.get("traces", []) + [trace]
            }

    # --- NODE 2: SEARCH AGENT ---
    def search_node(self, state: ResearchGraphState) -> Dict[str, Any]:
        tasks_data = state.get("planned_search_tasks", [])
        budget = state.get("search_budget_remaining", 5)
        executed = list(state.get("executed_queries", []))
        existing_results = list(state.get("search_results", []))
        errors = list(state.get("errors_and_warnings", []))
        traces = list(state.get("traces", []))

        searches_run = 0
        new_results = []
        urls_discovered = []

        for task_dict in tasks_data:
            q = task_dict["query"]
            if q in executed:
                continue

            if budget <= 0:
                errors.append("Search budget limit reached; skipping further web searches.")
                break

            try:
                # Execute targeted search via SerpApi
                resp = self.search_provider.search(q)
                executed.append(q)
                budget -= 1
                searches_run += 1

                for item in resp.items:
                    new_results.append(item.model_dump())
                    urls_discovered.append(item.url)

            except SerpApiException as serp_err:
                errors.append(f"SerpApi query error for '{q}': {str(serp_err)}")
                logger.warning(f"Search failed for '{q}': {serp_err}")
            except Exception as e:
                errors.append(f"Unexpected search failure for '{q}': {str(e)}")
                logger.error(f"Unexpected error searching '{q}': {e}")

        all_results = existing_results + new_results

        trace = _create_trace(
            stage="Search",
            agent_name="Search Agent",
            action="Execute Targeted Searches",
            summary=f"Executed {searches_run} queries. Found {len(new_results)} candidate source items. Budget remaining: {budget}.",
            details={"searches_executed": searches_run, "new_results_count": len(new_results), "budget_remaining": budget},
            source_urls=urls_discovered[:5]
        )
        traces.append(trace)

        return {
            "executed_queries": executed,
            "search_budget_remaining": budget,
            "search_results": all_results,
            "planned_search_tasks": [], # clear consumed tasks
            "errors_and_warnings": errors,
            "workflow_status": ResearchStatus.SEARCHING.value,
            "traces": traces
        }

    # --- NODE 3: EVIDENCE EXTRACTION AGENT ---
    def evidence_extraction_node(self, state: ResearchGraphState) -> Dict[str, Any]:
        search_results = state.get("search_results", [])
        retrieved_sources = list(state.get("retrieved_sources", []))
        extracted_evidence = list(state.get("extracted_evidence", []))
        candidate_requirements = list(state.get("candidate_requirements", []))
        errors = list(state.get("errors_and_warnings", []))
        traces = list(state.get("traces", []))
        profile = ApplicantProfile(**state["applicant_profile"])

        retrieved_urls = {s["metadata"]["url"] for s in retrieved_sources}
        new_sources_count = 0
        new_evidence_count = 0
        touched_urls = []
        evidence_ids = []

        # Sort search results so official sites are processed first
        sorted_results = sorted(search_results, key=lambda x: not x.get("is_official", False))

        for res in sorted_results:
            url = res["url"]
            if url in retrieved_urls:
                continue

            # Limit total sources retrieved per run to bounded maximum (e.g. 6)
            if len(retrieved_sources) >= 6:
                break

            # Secure retrieval through backend ingestion service
            source_obj = self.page_fetcher.fetch_source(url)
            retrieved_sources.append(source_obj.model_dump())
            retrieved_urls.add(url)
            new_sources_count += 1
            touched_urls.append(url)

            if not source_obj.is_accessible:
                errors.append(f"Source page inaccessible ({url}): {source_obj.error_message}")
                continue

            if source_obj.had_injection_attempt:
                errors.append(f"Security Alert: Untrusted prompt injection attempt neutralized in source {url}.")

            # Extract requirements and evidence excerpts
            ev_list, cand_list = RequirementExtractor.extract_from_source(source_obj, profile)

            for ev in ev_list:
                # Provenance check: verify verbatim quote in source
                if EvidenceValidator.verify_provenance(ev, source_obj):
                    extracted_evidence.append(ev.model_dump())
                    evidence_ids.append(ev.id)
                    new_evidence_count += 1

            for cand in cand_list:
                # Only add if candidate has verified supporting evidence
                if any(ev_id in evidence_ids for ev_id in cand.supporting_evidence_ids):
                    # Deduplicate candidate by title
                    if not any(c["title"] == cand.title for c in candidate_requirements):
                        candidate_requirements.append(cand.model_dump())

        trace = _create_trace(
            stage="Evidence Extraction",
            agent_name="Evidence Extraction Agent",
            action="Retrieve & Extract Evidence",
            summary=f"Retrieved {new_sources_count} sources. Extracted {new_evidence_count} verbatim evidence excerpts linked to sources.",
            details={"new_sources_count": new_sources_count, "new_evidence_count": new_evidence_count, "total_candidates": len(candidate_requirements)},
            source_urls=touched_urls,
            evidence_ids=evidence_ids
        )
        traces.append(trace)

        return {
            "retrieved_sources": retrieved_sources,
            "extracted_evidence": extracted_evidence,
            "candidate_requirements": candidate_requirements,
            "errors_and_warnings": errors,
            "workflow_status": ResearchStatus.EXTRACTING.value,
            "traces": traces
        }

    # --- NODE 4: REQUIREMENT VERIFICATION AGENT ---
    def requirement_verification_node(self, state: ResearchGraphState) -> Dict[str, Any]:
        candidate_data = state.get("candidate_requirements", [])
        evidence_data = state.get("extracted_evidence", [])
        profile = ApplicantProfile(**state["applicant_profile"])
        traces = list(state.get("traces", []))

        evidence_objs = [ExtractedEvidence(**e) for e in evidence_data]

        # 1. Detect Conflicts across sources
        conflicts = ConflictDetector.detect_conflicts(evidence_objs)
        conflicts_data = [c.model_dump() for c in conflicts]

        # 2. Deterministic Verification & Classification Policy
        validated_list: List[ValidatedRequirement] = []
        for c_dict in candidate_data:
            cand = CandidateRequirement(**c_dict)
            val = DeterministicClassifier.classify_requirement(cand, evidence_objs, profile)
            validated_list.append(val)

        # 3. Assess completeness & evidence gaps
        unresolved_questions: List[str] = []
        
        # Check user question
        user_q = state.get("user_question", "")
        if user_q:
            outcome, rationale, _ = EvidenceValidator.evaluate_claim(user_q, evidence_objs, conflicts, profile)
            if outcome in [ClaimOutcome.NOT_ESTABLISHED, ClaimOutcome.UNABLE_TO_VERIFY]:
                unresolved_questions.append(f"Insufficient proof to establish: {user_q}")

        # Check core requirements completeness
        validated_titles = {v.title for v in validated_list if v.classification in [RequirementClassification.MANDATORY, RequirementClassification.CONDITIONAL]}
        
        if "Proof of Financial Means (Bank Statements)" not in validated_titles:
            unresolved_questions.append("Required bank statement duration and financial proof threshold")
        if "Travel Health Insurance" not in validated_titles:
            unresolved_questions.append("Mandatory travel health insurance coverage limit")

        trace = _create_trace(
            stage="Verification",
            agent_name="Requirement Verification Agent",
            action="Validate Requirements & Detect Conflicts",
            summary=f"Validated {len(validated_list)} requirements via deterministic policy. Detected {len(conflicts)} conflicts. Found {len(unresolved_questions)} evidence gaps.",
            details={
                "validated_count": len(validated_list),
                "conflicts_count": len(conflicts),
                "gaps_count": len(unresolved_questions)
            }
        )
        traces.append(trace)

        return {
            "validated_classifications": [v.model_dump() for v in validated_list],
            "conflicting_evidence": conflicts_data,
            "unresolved_questions": unresolved_questions,
            "workflow_status": ResearchStatus.VERIFYING.value,
            "traces": traces
        }

    # --- EVALUATION NODE: ASSESS BOUNDS AND STOPPING CONDITIONS ---
    def completeness_evaluation_node(self, state: ResearchGraphState) -> Dict[str, Any]:
        iteration = state.get("iteration_count", 0)
        max_iter = state.get("max_iterations", 3)
        budget = state.get("search_budget_remaining", 5)
        gaps = state.get("unresolved_questions", [])
        executed = set(state.get("executed_queries", []))
        profile = ApplicantProfile(**state["applicant_profile"])
        traces = list(state.get("traces", []))

        should_refine = True
        stop_reason = None

        if not gaps:
            should_refine = False
            stop_reason = "Complete: All material research questions satisfied."
        elif iteration >= max_iter - 1:
            should_refine = False
            stop_reason = f"Bounded stop: Maximum research iterations reached ({max_iter})."
        elif budget <= 0:
            should_refine = False
            stop_reason = "Bounded stop: Search request budget exhausted."
        else:
            potential_gap_tasks = QueryBuilder.build_gap_queries(profile, gaps)
            unexecuted_tasks = [t for t in potential_gap_tasks if t.query not in executed]
            if not unexecuted_tasks:
                should_refine = False
                stop_reason = "Bounded stop: Duplicate-query prevention stopped further search loops."

        new_iteration = iteration + 1 if should_refine else iteration

        action_name = "Trigger Additional Research Loop" if should_refine else "Conclude Research Loop"
        summary_text = (
            f"Research loop iteration {iteration} evaluated. Triggering iteration {new_iteration} to resolve {len(gaps)} gaps."
            if should_refine
            else f"Research loop concluded: {stop_reason}"
        )

        trace = _create_trace(
            stage="Completeness Evaluation",
            agent_name="Research Orchestrator",
            action=action_name,
            summary=summary_text,
            details={
                "iteration": iteration,
                "next_iteration": new_iteration,
                "should_refine": should_refine,
                "gaps_count": len(gaps),
                "budget_remaining": budget,
                "stop_reason": stop_reason
            }
        )
        traces.append(trace)

        return {
            "iteration_count": new_iteration,
            "stop_reason": stop_reason,
            "should_refine": should_refine,
            "traces": traces,
            "workflow_status": ResearchStatus.EVALUATING.value if should_refine else ResearchStatus.GENERATING_CHECKLIST.value
        }

    # --- CONDITIONAL ROUTER ---
    def completeness_router(self, state: ResearchGraphState) -> str:
        if state.get("should_refine", False):
            return "research_planner"
        return "checklist_generator"

    # --- NODE 5: CHECKLIST GENERATION AGENT ---
    def checklist_generation_node(self, state: ResearchGraphState) -> Dict[str, Any]:
        val_data = state.get("validated_classifications", [])
        evidence_data = {e["id"]: e for e in state.get("extracted_evidence", [])}
        profile = ApplicantProfile(**state["applicant_profile"])
        run_id = state.get("run_id", str(uuid.uuid4()))
        unresolved = state.get("unresolved_questions", [])
        stop_reason = state.get("stop_reason") or "Completed research workflow."
        traces = list(state.get("traces", []))

        mandatory_items = []
        conditional_items = []
        recommended_items = []
        unverified_items = []

        for v_dict in val_data:
            v = ValidatedRequirement(**v_dict)

            # Build citations
            citations = []
            for ev_id in v.evidence_ids:
                if ev_id in evidence_data:
                    ev = evidence_data[ev_id]
                    citations.append(
                        ChecklistCitation(
                            source_title=ev["source_title"],
                            source_url=ev["source_url"],
                            quote=ev["exact_quote"],
                            is_official=ev["is_official"]
                        )
                    )

            item = ChecklistItem(
                id=f"chk_{uuid.uuid4().hex[:8]}",
                title=v.title,
                description=v.description,
                classification=v.classification,
                applies_to=f"Applicant ({profile.nationality} citizen, {profile.employment_status})",
                conditions=v.conditions,
                exceptions=v.exceptions,
                citations=citations,
                is_actionable=True
            )

            if v.classification == RequirementClassification.MANDATORY:
                mandatory_items.append(item)
            elif v.classification == RequirementClassification.CONDITIONAL:
                conditional_items.append(item)
            elif v.classification == RequirementClassification.RECOMMENDED:
                recommended_items.append(item)
            elif v.classification == RequirementClassification.UNVERIFIED:
                unverified_items.append(item)

        checklist = DocumentChecklist(
            id=f"cl_{uuid.uuid4().hex[:8]}",
            run_id=run_id,
            destination_country=profile.destination_country,
            visa_category=profile.visa_category,
            applicant_summary=f"{profile.employment_status} applicant traveling for {profile.planned_duration_days} days.",
            mandatory_items=mandatory_items,
            conditional_items=conditional_items,
            recommended_items=recommended_items,
            unverified_items=unverified_items,
            unresolved_questions=unresolved
        )

        trace = _create_trace(
            stage="Checklist Generation",
            agent_name="Checklist Generation Agent",
            action="Generate Personalized Document Checklist",
            summary=f"Synthesized checklist: {len(mandatory_items)} Mandatory, {len(conditional_items)} Conditional, {len(recommended_items)} Recommended, {len(unverified_items)} Unverified. Workflow stopped: {stop_reason}",
            details={
                "mandatory_count": len(mandatory_items),
                "conditional_count": len(conditional_items),
                "recommended_count": len(recommended_items),
                "unverified_count": len(unverified_items),
                "stop_reason": stop_reason
            }
        )
        traces.append(trace)

        return {
            "final_checklist": checklist.model_dump(),
            "stop_reason": stop_reason,
            "workflow_status": ResearchStatus.COMPLETED.value,
            "traces": traces
        }

    def run(self, initial_state: ResearchState) -> ResearchState:
        """Executes the full LangGraph state machine run."""
        state_dict: ResearchGraphState = initial_state.model_dump()
        final_dict = self.app.invoke(state_dict)
        return ResearchState(**final_dict)
