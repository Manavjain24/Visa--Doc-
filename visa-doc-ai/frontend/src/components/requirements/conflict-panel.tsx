import { ConflictRecord } from "@/types/research";

export function ConflictPanel({ conflicts }: { conflicts: ConflictRecord[] }) {
  if (!conflicts || conflicts.length === 0) return null;

  return (
    <div className="rounded-xl border border-amber-300 bg-amber-50 p-5 mb-6">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-lg">⚠️</span>
        <h3 className="font-semibold text-amber-900 text-sm">
          Detected Source Discrepancies ({conflicts.length})
        </h3>
      </div>
      <div className="space-y-4">
        {conflicts.map((c, i) => (
          <div key={i} className="bg-white/80 rounded-lg p-3 text-xs border border-amber-200">
            <p className="font-medium text-amber-950 mb-1">{c.requirement_title}</p>
            <p className="text-amber-800 mb-2">Issue: {c.issue}</p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-slate-600 mb-2">
              <div className="p-2 bg-slate-50 rounded border border-slate-200">
                <span className="font-semibold block text-slate-800 truncate">Source A ({c.source_a_url}):</span>
                &quot;{c.source_a_claim}&quot;
              </div>
              <div className="p-2 bg-slate-50 rounded border border-slate-200">
                <span className="font-semibold block text-slate-800 truncate">Source B ({c.source_b_url}):</span>
                &quot;{c.source_b_claim}&quot;
              </div>
            </div>
            <p className="text-emerald-800 font-medium bg-emerald-50 p-1.5 rounded">
              Resolution Strategy: {c.resolution_strategy}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
