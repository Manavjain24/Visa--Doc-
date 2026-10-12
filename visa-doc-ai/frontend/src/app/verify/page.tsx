"use client";

import { useState } from "react";
import { PageContainer } from "@/components/layout/page-container";
import { verifyClaim } from "@/lib/api-client";
import { VerificationResult } from "@/types/research";
import { RequirementBadge } from "@/components/requirements/requirement-badge";

export default function VerifyPage() {
  const [claim, setClaim] = useState("Is travel health insurance mandatory for Schengen visa?");
  const [destination, setDestination] = useState("Germany");
  const [result, setResult] = useState<VerificationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleVerify = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const res = await verifyClaim({
        applicant_profile: {
          nationality: "India",
          residence_country: "India",
          destination_country: destination,
          visa_category: "Tourist",
          purpose_of_travel: "Tourism",
          planned_duration_days: 14,
          employment_status: "Employed",
          financial_sponsor: "Self",
          has_previous_visas: false,
          special_circumstances: [],
          specific_questions: [],
        },
        claim_statement: claim,
      });
      setResult(res);
    } catch (err: any) {
      setError(err.message || "Verification request failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageContainer>
      <div className="max-w-3xl mx-auto space-y-6">
        <div>
          <h1 className="text-xl font-bold text-slate-900">Visa Requirement Claim Verifier</h1>
          <p className="text-xs text-slate-500 mt-1">
            Test any requirement claim directly against verified evidence and official sources.
          </p>
        </div>

        <form onSubmit={handleVerify} className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Destination Country</label>
            <input
              type="text"
              value={destination}
              onChange={(e) => setDestination(e.target.value)}
              className="w-full text-xs px-3.5 py-2.5 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Requirement Claim to Verify</label>
            <textarea
              rows={3}
              value={claim}
              onChange={(e) => setClaim(e.target.value)}
              placeholder="e.g. Police clearance certificate is required for tourist visit"
              className="w-full text-xs px-3.5 py-2.5 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          {error && <div className="p-3 bg-red-50 text-red-700 rounded-lg text-xs">{error}</div>}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg text-xs transition-colors disabled:opacity-50"
          >
            {loading ? "Evaluating Claim against Official Evidence..." : "Verify Claim Outcome"}
          </button>
        </form>

        {result && (
          <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Outcome</span>
              <RequirementBadge classification={result.classification} />
            </div>

            <div className="space-y-1">
              <span className="text-xs font-bold text-slate-800">{result.outcome}</span>
              <p className="text-xs text-slate-600 leading-relaxed">{result.rationale}</p>
            </div>

            {result.supporting_evidence && result.supporting_evidence.length > 0 && (
              <div className="pt-3 border-t border-slate-100 space-y-2">
                <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block">
                  Supporting Evidence Passages
                </span>
                {result.supporting_evidence.map((ev, i) => (
                  <div key={i} className="bg-slate-50 p-3 rounded-lg border border-slate-200 text-xs">
                    <p className="italic text-slate-700 mb-1">&quot;{ev.exact_quote}&quot;</p>
                    <a
                      href={ev.source_url}
                      target="_blank"
                      rel="noreferrer"
                      className="text-[10px] text-indigo-600 hover:underline block truncate"
                    >
                      Source: {ev.source_url}
                    </a>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </PageContainer>
  );
}
