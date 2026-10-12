"use client";

import { useEffect } from "react";
import { PageContainer } from "@/components/layout/page-container";

export default function ErrorPage({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <PageContainer>
      <div className="max-w-md mx-auto text-center py-12 space-y-4">
        <h2 className="text-lg font-bold text-slate-900">Something went wrong</h2>
        <p className="text-xs text-slate-600">{error.message || "An unexpected error occurred."}</p>
        <button
          onClick={() => reset()}
          className="px-4 py-2 bg-indigo-600 text-white text-xs font-semibold rounded-lg hover:bg-indigo-700"
        >
          Try again
        </button>
      </div>
    </PageContainer>
  );
}
