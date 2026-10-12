import { RequirementClassification } from "@/types/research";

export function RequirementBadge({ classification }: { classification: RequirementClassification }) {
  const styles: Record<RequirementClassification, string> = {
    Mandatory: "bg-red-50 text-red-700 border-red-200",
    Conditional: "bg-amber-50 text-amber-700 border-amber-200",
    Recommended: "bg-blue-50 text-blue-700 border-blue-200",
    Unverified: "bg-slate-100 text-slate-700 border-slate-200",
    "Not applicable": "bg-gray-100 text-gray-500 border-gray-200 line-through",
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${
        styles[classification] || styles.Unverified
      }`}
    >
      {classification}
    </span>
  );
}
