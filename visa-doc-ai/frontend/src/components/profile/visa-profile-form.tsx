"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { ApplicantProfile } from "@/types/research";
import { startResearch } from "@/lib/api-client";

export function VisaProfileForm() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState<ApplicantProfile>({
    nationality: "India",
    residence_country: "India",
    destination_country: "Germany",
    visa_category: "Tourist",
    purpose_of_travel: "Vacation and tourism",
    planned_duration_days: 14,
    employment_status: "Employed",
    financial_sponsor: "Self",
    has_previous_visas: false,
    special_circumstances: [],
    specific_questions: [],
  });

  const [question, setQuestion] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const state = await startResearch(formData, question);
      router.push(`/research/${state.run_id}`);
    } catch (err: any) {
      setError(err.message || "Failed to start research");
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-xl border border-slate-200 p-8 shadow-sm space-y-6">
      <div>
        <h2 className="text-lg font-bold text-slate-900">Applicant Travel Profile</h2>
        <p className="text-xs text-slate-500">
          Enter applicant details to run multi-stage agentic research against official immigration sources.
        </p>
      </div>

      {error && (
        <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-xs text-red-700">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1.5">Citizenship / Passport</label>
          <input
            type="text"
            required
            value={formData.nationality}
            onChange={(e) => setFormData({ ...formData, nationality: e.target.value })}
            className="w-full text-xs px-3.5 py-2.5 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1.5">Residence Country</label>
          <input
            type="text"
            required
            value={formData.residence_country}
            onChange={(e) => setFormData({ ...formData, residence_country: e.target.value })}
            className="w-full text-xs px-3.5 py-2.5 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1.5">Destination Country</label>
          <input
            type="text"
            required
            value={formData.destination_country}
            onChange={(e) => setFormData({ ...formData, destination_country: e.target.value })}
            className="w-full text-xs px-3.5 py-2.5 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1.5">Visa Category</label>
          <select
            value={formData.visa_category}
            onChange={(e) => setFormData({ ...formData, visa_category: e.target.value })}
            className="w-full text-xs px-3.5 py-2.5 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="Tourist">Tourist / Short Stay (Schengen C)</option>
            <option value="Business">Business Visa</option>
            <option value="Student">Student Visa</option>
            <option value="Work">Work / Employment Visa</option>
          </select>
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1.5">Employment Status</label>
          <select
            value={formData.employment_status}
            onChange={(e) => setFormData({ ...formData, employment_status: e.target.value })}
            className="w-full text-xs px-3.5 py-2.5 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="Employed">Employed (Salaried)</option>
            <option value="Self-Employed">Self-Employed / Business Owner</option>
            <option value="Student">Enrolled Student</option>
            <option value="Unemployed">Unemployed</option>
            <option value="Retired">Retired</option>
          </select>
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1.5">Planned Duration (Days)</label>
          <input
            type="number"
            min="1"
            max="365"
            value={formData.planned_duration_days}
            onChange={(e) => setFormData({ ...formData, planned_duration_days: parseInt(e.target.value) || 1 })}
            className="w-full text-xs px-3.5 py-2.5 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
      </div>

      <div>
        <label className="block text-xs font-semibold text-slate-700 mb-1.5">
          Specific Question to Investigate (Optional)
        </label>
        <input
          type="text"
          placeholder="e.g. Is an employer leave letter mandatory, or how many months of bank statements are needed?"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="w-full text-xs px-3.5 py-2.5 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
      </div>

      <div className="pt-2">
        <button
          type="submit"
          disabled={loading}
          className="w-full py-3 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs tracking-wide shadow-sm transition-colors disabled:opacity-50"
        >
          {loading ? "Initializing Agentic Research Run..." : "Run Evidence-Grounded Research & Verification"}
        </button>
      </div>
    </form>
  );
}
