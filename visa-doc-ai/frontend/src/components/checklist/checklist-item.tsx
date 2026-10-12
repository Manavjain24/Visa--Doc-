import { ChecklistItem } from "@/types/research";
import { RequirementBadge } from "@/components/requirements/requirement-badge";

export function ChecklistItemCard({ item }: { item: ChecklistItem }) {
  return (
    <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm space-y-3">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="space-y-1">
          <h4 className="font-semibold text-slate-900 text-sm">{item.title}</h4>
          <p className="text-xs text-slate-600 leading-relaxed">{item.description}</p>
        </div>
        <RequirementBadge classification={item.classification} />
      </div>

      {item.conditions && item.conditions.length > 0 && (
        <div className="bg-amber-50/60 border border-amber-200 rounded-lg p-2.5 text-xs text-amber-900">
          <span className="font-semibold block mb-1">Applicable Conditions:</span>
          <ul className="list-disc list-inside space-y-0.5 text-amber-800">
            {item.conditions.map((c, i) => (
              <li key={i}>{c}</li>
            ))}
          </ul>
        </div>
      )}

      {item.citations && item.citations.length > 0 && (
        <div className="space-y-1.5 pt-2 border-t border-slate-100">
          <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block">
            Official Evidence Citations
          </span>
          <div className="space-y-1.5">
            {item.citations.map((c, i) => (
              <div key={i} className="text-xs bg-slate-50 p-2.5 rounded border border-slate-200">
                <blockquote className="italic text-slate-700 mb-1">&quot;{c.quote}&quot;</blockquote>
                <div className="flex items-center justify-between text-[11px] text-slate-500">
                  <span className="font-medium text-slate-700">{c.source_title}</span>
                  <a
                    href={c.source_url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-indigo-600 hover:underline font-mono"
                  >
                    View Source &rarr;
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
