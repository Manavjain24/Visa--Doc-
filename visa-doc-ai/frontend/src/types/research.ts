export type RequirementClassification =
  | "Mandatory"
  | "Conditional"
  | "Recommended"
  | "Unverified"
  | "Not applicable";

export type ClaimOutcome =
  | "Supported by official evidence"
  | "Supported only under specified conditions"
  | "Not established by sources reviewed"
  | "Conflicting official information"
  | "Unable to verify";

export type ResearchStatus =
  | "initializing"
  | "planning"
  | "searching"
  | "extracting"
  | "verifying"
  | "evaluating"
  | "generating_checklist"
  | "completed"
  | "failed"
  | "exhausted_budget";

export interface ApplicantProfile {
  id?: string;
  nationality: string;
  residence_country: string;
  destination_country: string;
  visa_category: string;
  purpose_of_travel: string;
  planned_duration_days: number;
  employment_status: string;
  financial_sponsor: string;
  has_previous_visas: boolean;
  special_circumstances: string[];
  specific_questions: string[];
}

export interface SearchResultItem {
  title: string;
  url: string;
  snippet: string;
  source_domain: string;
  is_official: boolean;
  rank: number;
  query: string;
  retrieved_at: string;
}

export interface SourceMetadata {
  url: string;
  domain: string;
  title: string;
  is_official: boolean;
  tier: string;
  http_status: number;
  content_type: string;
  retrieved_at: string;
}

export interface RetrievedSource {
  id: string;
  metadata: SourceMetadata;
  raw_text: string;
  is_accessible: boolean;
  error_message?: string;
  had_injection_attempt: boolean;
}

export interface ExtractedEvidence {
  id: string;
  source_id: string;
  source_url: string;
  source_title: string;
  is_official: boolean;
  exact_quote: string;
  char_offset_start: number;
  char_offset_end: number;
  applicable_categories: string[];
  applicable_conditions: string[];
  extracted_at: string;
}

export interface ValidatedRequirement {
  id: string;
  candidate_id: string;
  title: string;
  description: string;
  classification: RequirementClassification;
  verification_outcome: ClaimOutcome;
  confidence_score: number;
  conditions: string[];
  exceptions: string[];
  evidence_ids: string[];
  source_urls: string[];
  deterministic_rationale: string;
}

export interface ConflictRecord {
  requirement_title: string;
  issue: string;
  source_a_url: string;
  source_a_claim: string;
  source_b_url: string;
  source_b_claim: string;
  resolution_strategy: string;
}

export interface ChecklistCitation {
  source_title: string;
  source_url: string;
  quote: string;
  is_official: boolean;
}

export interface ChecklistItem {
  id: string;
  title: string;
  description: string;
  classification: RequirementClassification;
  applies_to: string;
  conditions: string[];
  exceptions: string[];
  citations: ChecklistCitation[];
  is_actionable: boolean;
}

export interface DocumentChecklist {
  id: string;
  run_id: string;
  destination_country: string;
  visa_category: string;
  applicant_summary: string;
  mandatory_items: ChecklistItem[];
  conditional_items: ChecklistItem[];
  recommended_items: ChecklistItem[];
  unverified_items: ChecklistItem[];
  unresolved_questions: string[];
  disclaimer: string;
  generated_at: string;
}

export interface ResearchTraceEntry {
  id: string;
  timestamp: string;
  stage: string;
  agent_name: string;
  action: string;
  summary: string;
  details: Record<string, any>;
  evidence_ids: string[];
  source_urls: string[];
}

export interface ResearchState {
  run_id: string;
  applicant_profile: ApplicantProfile;
  user_question: string;
  research_objectives: string[];
  planned_search_tasks: Array<{ query: string; objective: string }>;
  executed_queries: string[];
  search_results: SearchResultItem[];
  retrieved_sources: RetrievedSource[];
  extracted_evidence: ExtractedEvidence[];
  candidate_requirements: any[];
  validated_classifications: ValidatedRequirement[];
  unresolved_questions: string[];
  conflicting_evidence: ConflictRecord[];
  iteration_count: number;
  max_iterations: number;
  search_budget_remaining: number;
  max_search_budget: number;
  stop_reason?: string;
  errors_and_warnings: string[];
  traces: ResearchTraceEntry[];
  final_checklist?: DocumentChecklist;
  workflow_status: ResearchStatus;
  created_at: string;
  updated_at: string;
}

export interface VerificationRequest {
  applicant_profile: ApplicantProfile;
  claim_statement: string;
}

export interface VerificationResult {
  claim_statement: string;
  outcome: ClaimOutcome;
  classification: RequirementClassification;
  is_verified: boolean;
  rationale: string;
  supporting_evidence: ExtractedEvidence[];
  conflicting_evidence: ConflictRecord[];
  sources_consulted: string[];
}
