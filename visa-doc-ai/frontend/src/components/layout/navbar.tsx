import Link from "next/link";

export function Navbar() {
  return (
    <header className="border-b border-slate-200 bg-white sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white font-bold text-lg">
            V
          </div>
          <span className="font-semibold text-lg tracking-tight text-slate-900">
            VisaDoc <span className="text-indigo-600">AI</span>
          </span>
        </Link>
        <nav className="flex items-center gap-6 text-sm font-medium text-slate-600">
          <Link href="/" className="hover:text-indigo-600 transition-colors">
            Research Assistant
          </Link>
          <Link href="/verify" className="hover:text-indigo-600 transition-colors">
            Claim Verifier
          </Link>
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800">
            Evidence-Grounded
          </span>
        </nav>
      </div>
    </header>
  );
}
