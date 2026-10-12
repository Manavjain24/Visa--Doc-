import { ResearchTraceEntry, ResearchStatus } from "@/types/research";

export function ResearchProgress({
  status,
  traces,
  iteration,
  maxIterations,
  budgetRemaining,
}: {
  status: ResearchStatus;
  traces: ResearchTraceEntry[];
  iteration: number;
  maxIterations: number;
  budgetRemaining: number;
}) {
  const stageBadges: Record<string, string> = {
    Planning: "bg-purple-100 text-purple-800",
    Refinement: "bg-purple-100 text-purple-800",
    Search: "bg-blue-100 text-blue-800",
    "Evidence Extraction": "bg-amber-100 text-amber-800",
    Verification: "bg-indigo-100 text-indigo-800",
    "Completeness Evaluation": "bg-teal-100 text-teal-800",
    "Checklist Generation": "bg-emerald-100 text-emerald-800",
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm mb-6">
      <div className="flex flex-wrap items-center justify-between gap-4 mb-4 pb-4 border-b border-slate-100">
        <div>
          <h2 className="text-base font-semibold text-slate-900">Agentic Research Orchestrator</h2>
          <p className="text-xs text-slate-500">Live Multi-Stage State Graph Execution</p>
        </div>
        <div className="flex items-center gap-3 text-xs">
          <span className="px-2.5 py-1 rounded bg-slate-100 font-mono text-slate-700">
            Loop: {iteration} / {maxIterations}
          </span>
          <span className="px-2.5 py-1 rounded bg-slate-100 font-mono text-slate-700">
            SerpApi Budget: {budgetRemaining} left
          </span>
          <span className="px-2.5 py-1 rounded bg-emerald-100 text-emerald-800 font-semibold uppercase">
            {status}
          </span>
        </div>
      </div>

      <div className="space-y-3">
        <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Workflow Trace Log</h3>
        <div className="space-y-2 max-h-96 overflow-y-auto pr-2">
          {traces.map((trace) => (
            <div
              key={trace.id}
              className="p-3 rounded-lg border border-slate-100 bg-slate-50/70 text-xs flex flex-col gap-1.5"
            >
              <div className="flex items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <span className={`px-2 py-0.5 rounded text-[11px] font-medium ${stageBadges[trace.stage] || "bg-slate-200"}`}>
                    {trace.stage}
                  </span>
                  <span className="font-semibold text-slate-800">{trace.agent_name}</span>
                </div>
                <span className="text-[10px] text-slate-400 font-mono">
                  {new Date(trace.timestamp).toLocaleTimeString()}
                </span>
              </div>
              <p className="text-slate-700">{trace.summary}</p>
              {trace.source_urls && trace.source_urls.length > 0 && (
                <div className="flex flex-wrap gap-1 mt-1">
                  {trace.source_urls.map((u, i) => (
                    <a
                      key={i}
                      href={u}
                      target="_blank"
                      rel="noreferrer"
                      className="text-[10px] text-indigo-600 hover:underline bg-white px-1.5 py-0.5 rounded border border-slate-200 truncate max-w-xs"
                    >
                      {u}
                    </a>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
