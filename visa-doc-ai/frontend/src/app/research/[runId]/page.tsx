"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { ResearchState } from "@/types/research";
import { getResearchState } from "@/lib/api-client";
import { PageContainer } from "@/components/layout/page-container";
import { ResearchProgress } from "@/components/research/research-progress";
import { ConflictPanel } from "@/components/requirements/conflict-panel";
import { ChecklistView } from "@/components/checklist/checklist-view";

export default function ResearchRunPage() {
  const params = useParams();
  const runId = params.runId as string;
  const [state, setState] = useState<ResearchState | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!runId) return;

    const fetchState = async () => {
      try {
        const data = await getResearchState(runId);
        setState(data);
      } catch (err: any) {
        setError(err.message || "Failed to load research run");
      }
    };

    fetchState();
  }, [runId]);

  if (error) {
    return (
      <PageContainer>
        <div className="p-6 bg-red-50 border border-red-200 rounded-xl text-xs text-red-700">
          {error}
        </div>
      </PageContainer>
    );
  }

  if (!state) {
    return (
      <PageContainer>
        <div className="text-center py-12 text-xs text-slate-500">
          Loading research execution state...
        </div>
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      <div className="space-y-6">
        <ResearchProgress
          status={state.workflow_status}
          traces={state.traces}
          iteration={state.iteration_count}
          maxIterations={state.max_iterations}
          budgetRemaining={state.search_budget_remaining}
        />

        <ConflictPanel conflicts={state.conflicting_evidence} />

        {state.final_checklist && <ChecklistView checklist={state.final_checklist} />}
      </div>
    </PageContainer>
  );
}
