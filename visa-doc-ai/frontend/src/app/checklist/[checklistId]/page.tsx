"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { DocumentChecklist } from "@/types/research";
import { getChecklist } from "@/lib/api-client";
import { PageContainer } from "@/components/layout/page-container";
import { ChecklistView } from "@/components/checklist/checklist-view";

export default function ChecklistPage() {
  const params = useParams();
  const checklistId = params.checklistId as string;
  const [checklist, setChecklist] = useState<DocumentChecklist | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!checklistId) return;
    getChecklist(checklistId)
      .then(setChecklist)
      .catch((err) => setError(err.message));
  }, [checklistId]);

  if (error) {
    return (
      <PageContainer>
        <div className="p-6 bg-red-50 border border-red-200 rounded-xl text-xs text-red-700">
          {error}
        </div>
      </PageContainer>
    );
  }

  if (!checklist) {
    return (
      <PageContainer>
        <div className="text-center py-12 text-xs text-slate-500">Loading checklist...</div>
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      <ChecklistView checklist={checklist} />
    </PageContainer>
  );
}
