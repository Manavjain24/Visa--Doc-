import { ApplicantProfile, ResearchState, VerificationRequest, VerificationResult, DocumentChecklist } from "@/types/research";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/v1";

export async function startResearch(
  profile: ApplicantProfile,
  userQuestion: string = "",
  maxIterations: number = 3,
  maxSearchBudget: number = 5
): Promise<ResearchState> {
  const res = await fetch(`${API_BASE}/research/start`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      applicant_profile: profile,
      user_question: userQuestion,
      max_iterations: maxIterations,
      max_search_budget: maxSearchBudget,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Failed to start research" }));
    throw new Error(err.detail || "Failed to start research");
  }
  return res.json();
}

export async function getResearchState(runId: string): Promise<ResearchState> {
  const res = await fetch(`${API_BASE}/research/${runId}`);
  if (!res.ok) {
    throw new Error(`Research run ${runId} not found`);
  }
  return res.json();
}

export async function listResearchRuns(): Promise<any[]> {
  const res = await fetch(`${API_BASE}/research`);
  if (!res.ok) return [];
  return res.json();
}

export async function verifyClaim(req: VerificationRequest): Promise<VerificationResult> {
  const res = await fetch(`${API_BASE}/verification/verify-claim`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
  if (!res.ok) {
    throw new Error("Verification request failed");
  }
  return res.json();
}

export async function getChecklist(checklistId: string): Promise<DocumentChecklist> {
  const res = await fetch(`${API_BASE}/checklists/${checklistId}`);
  if (!res.ok) {
    throw new Error(`Checklist ${checklistId} not found`);
  }
  return res.json();
}

export async function getChecklistForRun(runId: string): Promise<DocumentChecklist> {
  const res = await fetch(`${API_BASE}/checklists/run/${runId}`);
  if (!res.ok) {
    throw new Error(`Checklist for run ${runId} not found`);
  }
  return res.json();
}
