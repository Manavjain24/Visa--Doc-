# VisaDoc AI

> **Bounded, Multi-Stage Agentic Research & Verification System for Visa Requirements**

VisaDoc AI is an evidence-grounded visa document assistant. Rather than generating ungrounded requirements or relying on decorative chatbots, VisaDoc AI coordinates five distinct, bounded logical agents using **LangGraph**, executes real Google Searches via **SerpApi**, retrieves source pages through a secure ingestion engine, and enforces a **deterministic verification layer** before producing personalized checklists.

---

## 🌟 Key Architecture & Highlights

### 1. Multi-Stage Logical Agents (LangGraph Orchestrator)
1. **Research Planner Agent:** Formulates objectives, identifies jurisdiction & profile conditions, tracks evidence gaps, and plans targeted searches. *(Does not invent rules without proof).*
2. **Search Agent:** Dispatches targeted queries to official government portals via **SerpApi**, deduplicates URLs, tracks timestamps, and enforces search budgets.
3. **Evidence Extraction Agent:** Ingests official HTML & PDF documents safely (SSRF-protected), records exact character offsets for verbatim quotes, and defuses prompt injection attempts.
4. **Requirement Verification Agent:** Evaluates evidence against candidate requirements, detects discrepancies across sources, and invokes the **deterministic verification policy**.
5. **Checklist Generation Agent:** Generates personalized checklists with verbatim citations, condition criteria, and transparent legal disclaimers.

```
Research Plan ──► SerpApi Search ──► Ingestion & Extraction ──► Verification & Conflict Check
      ▲                                                                     │
      │                                                                     ▼
      └───────── Bounded Feedback Loop (Gaps / Budget) ◄───────── Completeness Evaluator
                                                                            │
                                                                            ▼
                                                               Checklist Generation ──► END
```

### 2. Deterministic Verification & Evidence Integrity
- **Strict Classification Policy:**
  - `Mandatory`: Verified by official government/embassy evidence for all applicants.
  - `Conditional`: Applies specifically to profile attributes (e.g., employment, sponsorship, minors).
  - `Recommended`: Advised or optional documents.
  - `Unverified`: Insufficient or unofficial evidence.
  - `Not applicable`: Excluded based on profile circumstances.
- **Rule of Non-Equivalence:** Missing search results are **never** treated as proof that a document is unnecessary.
- **Conflict Detector:** Identifies and documents contradictory guidelines between sources (e.g. 3-month vs. 6-month bank statements) with precedence resolution.

### 3. Safety, Bounding & Observability
- **Hard Resource Limits:** Maximum iterations (`RESEARCH_MAX_ITERATIONS=3`) and SerpApi request budgets (`RESEARCH_MAX_SEARCH_BUDGET=5`).
- **Server-Side Secrets:** SerpApi credentials remain strictly on the backend.
- **SSRF Defense:** Blocks private IPs, loopbacks, link-local addresses, and cloud metadata endpoints.
- **Prompt Injection Neutralization:** Treats all third-party web content as untrusted evidentiary data.
- **Observability:** Step-by-step trace logs exposed to the UI without logging API keys or private applicant data.

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.11+**
- **Node.js 18+** & **npm**

---

### Backend Setup (FastAPI & LangGraph)

1. Open PowerShell and navigate to `backend`:
   ```powershell
   cd backend
   ```

2. Install dependencies:
   ```powershell
   py -m pip install -r requirements.txt
   ```

3. Configure environment variables:
   Copy `.env.example` to `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```
   *Edit `.env` to add your optional `SERPAPI_API_KEY` (offline tests run with built-in mock fixtures).*

4. Start the backend API:
   ```powershell
   py -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```
   - **Health Endpoint:** [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
   - **Swagger Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### Frontend Setup (Next.js & Tailwind CSS)

1. Open a new terminal and navigate to `frontend`:
   ```powershell
   cd frontend
   ```

2. Install dependencies:
   ```powershell
   npm install
   ```

3. Start development server:
   ```powershell
   npm run dev
   ```
   - **Web Application:** [http://localhost:3000](http://localhost:3000)

---

## 🧪 Running Automated Tests

The test suite covers edge cases including missing credentials, search failures, inaccessible sources, contradictory sources, duplicate-query prevention, and prompt injection defense:

```powershell
cd backend
py -m pytest -v
```

**Results:** 26/26 tests passing (100% pass rate).

---

## 📁 Repository Structure

```
visa-doc-ai/
├── backend/
│   ├── app/
│   │   ├── ai/            # Prompts and LLM provider abstractions
│   │   ├── api/v1/        # FastAPI routers (research, verification, checklists, profiles)
│   │   ├── core/          # Settings, sanitized logging, and security validators
│   │   ├── db/            # SQLAlchemy database engine and session
│   │   ├── ingestion/     # SSRF-safe page fetcher, HTML and PDF text extractors
│   │   ├── models/        # Database models
│   │   ├── schemas/       # Typed Pydantic models and shared research state
│   │   ├── search/        # SerpApi provider, cache, and query builder
│   │   ├── services/      # LangGraph orchestrator and business logic
│   │   └── verification/  # Deterministic classifier, conflict detector, and evidence validator
│   ├── tests/             # Pytest suite with fixtures and mocks
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/           # Next.js App Router (research, verify, checklists)
│   │   ├── components/    # UI, progress trace, and checklist components
│   │   ├── lib/           # API client and utility functions
│   │   └── types/         # TypeScript interface definitions
│   └── package.json
└── docs/                  # Architecture and implementation notes
```

---

## ⚖️ Legal Disclaimer

VisaDoc AI provides automated research and synthesis based on publicly accessible immigration guidelines. It **does not** constitute legal immigration advice and **cannot guarantee** visa approval. Consular officers retain absolute discretion over visa adjudication.
