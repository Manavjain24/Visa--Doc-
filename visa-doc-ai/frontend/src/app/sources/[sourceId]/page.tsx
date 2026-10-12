"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { PageContainer } from "@/components/layout/page-container";

export default function SourceDetailPage() {
  const params = useParams();
  const sourceId = params.sourceId as string;
  const [source, setSource] = useState<any>(null);

  useEffect(() => {
    if (!sourceId) return;
    fetch(`http://127.0.0.1:8000/api/v1/sources/${sourceId}`)
      .then((res) => res.json())
      .then(setSource)
      .catch(console.error);
  }, [sourceId]);

  return (
    <PageContainer>
      <div className="max-w-3xl mx-auto space-y-4">
        <h1 className="text-lg font-bold text-slate-900">Retrieved Source Details</h1>
        {source ? (
          <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm space-y-3 text-xs">
            <h2 className="font-semibold text-sm text-slate-800">{source.title}</h2>
            <p className="text-slate-500 font-mono">{source.url}</p>
            <div className="p-3 bg-slate-50 rounded border border-slate-200 whitespace-pre-wrap font-mono text-[11px] max-h-96 overflow-y-auto">
              {source.raw_text}
            </div>
          </div>
        ) : (
          <p className="text-xs text-slate-500">Loading source details...</p>
        )}
      </div>
    </PageContainer>
  );
}
