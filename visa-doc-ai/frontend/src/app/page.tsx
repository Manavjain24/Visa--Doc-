import { PageContainer } from "@/components/layout/page-container";
import { VisaProfileForm } from "@/components/profile/visa-profile-form";

export default function Home() {
  return (
    <PageContainer>
      <div className="max-w-3xl mx-auto space-y-6">
        <div className="text-center space-y-2 py-4">
          <span className="text-xs font-bold tracking-wider text-indigo-600 uppercase bg-indigo-50 px-3 py-1 rounded-full">
            Agentic Research System
          </span>
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
            Official Visa Document Verification
          </h1>
          <p className="text-xs text-slate-600 max-w-xl mx-auto leading-relaxed">
            Multi-stage LangGraph orchestrator backed by real SerpApi Google Search, secure content extraction,
            and deterministic classification policies.
          </p>
        </div>
        <VisaProfileForm />
      </div>
    </PageContainer>
  );
}
