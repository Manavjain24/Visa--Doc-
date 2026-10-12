"use client";

import { useState } from "react";
import { DocumentChecklist } from "@/types/research";
import { ChecklistItemCard } from "@/components/checklist/checklist-item";

export function ChecklistView({ checklist }: { checklist: DocumentChecklist }) {
  const [filter, setFilter] = useState<string>("all");

  const allItems = [
    ...checklist.mandatory_items,
    ...checklist.conditional_items,
    ...checklist.recommended_items,
    ...checklist.unverified_items,
  ];

  const filteredItems = allItems.filter((item) => {
    if (filter === "all") return true;
    return item.classification.toLowerCase() === filter.toLowerCase();
  });

  return (
    <div className="space-y-6">
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-4 mb-4">
          <div>
            <h1 className="text-xl font-bold text-slate-900">
              Personalized Document Checklist
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Destination: {checklist.destination_country} • Category: {checklist.visa_category} • {checklist.applicant_summary}
            </p>
          </div>
          <div className="flex items-center gap-2">
            {["all", "mandatory", "conditional", "recommended", "unverified"].map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium capitalize transition-colors ${
                  filter === f
                    ? "bg-indigo-600 text-white"
                    : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                }`}
              >
                {f}
              </button>
            ))}
          </div>
        </div>

        <div className="p-3.5 bg-amber-50 border border-amber-200 rounded-lg text-xs text-amber-900">
          <p className="font-semibold mb-0.5">Legal Disclaimer</p>
          <p className="text-amber-800 leading-relaxed">{checklist.disclaimer}</p>
        </div>
      </div>

      {checklist.unresolved_questions && checklist.unresolved_questions.length > 0 && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-5">
          <h3 className="text-xs font-bold text-red-900 uppercase tracking-wider mb-2">
            Unresolved Research Questions / Evidence Gaps
          </h3>
          <ul className="list-disc list-inside text-xs text-red-800 space-y-1">
            {checklist.unresolved_questions.map((q, i) => (
              <li key={i}>{q}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="space-y-4">
        {filteredItems.map((item) => (
          <ChecklistItemCard key={item.id} item={item} />
        ))}
      </div>
    </div>
  );
}
