import Link from "next/link";
import { PageContainer } from "@/components/layout/page-container";

export default function NotFound() {
  return (
    <PageContainer>
      <div className="max-w-md mx-auto text-center py-12 space-y-4">
        <h2 className="text-xl font-bold text-slate-900">404 - Page Not Found</h2>
        <p className="text-xs text-slate-600">The requested visa research resource does not exist.</p>
        <Link
          href="/"
          className="inline-block px-4 py-2 bg-indigo-600 text-white text-xs font-semibold rounded-lg hover:bg-indigo-700"
        >
          Return to Assistant
        </Link>
      </div>
    </PageContainer>
  );
}
