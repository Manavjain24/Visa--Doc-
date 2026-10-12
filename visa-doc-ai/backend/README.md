# VisaDoc AI

Evidence-grounded, bounded multi-stage agentic research and verification system for visa documents.

## Key Features

1. **Multi-Stage LangGraph Orchestrator:**
   - **Research Planner Agent:** Analyzes applicant profile, identifies missing evidence, and schedules targeted search queries.
   - **Search Agent:** Real SerpApi Google Search provider with official domain prioritization, strict caching, and query deduplication.
   - **Evidence Extraction Agent:** Secure SSRF-protected backend ingestion (HTML & PDF), verbatim quote offset provenance tracking, and prompt injection neutralization.
   - **Requirement Verification Agent:** Deterministic classification policy (Mandatory, Conditional, Recommended, Unverified, Not applicable), discrepancy detection, and honest missing evidence reporting.
   - **Checklist Generation Agent:** Synthesizes actionable personalized document checklists with verbatim citations and legal disclaimers.
2. **Bounded Feedback Loop:**
   - Configurable maximum research iterations (`RESEARCH_MAX_ITERATIONS=3`).
   - Configurable maximum search budget (`RESEARCH_MAX_SEARCH_BUDGET=5`).
   - Duplicate-query prevention and explicit stopping conditions.
3. **Traceability & Observability:**
   - Every requirement is traceable to verbatim excerpts from retrieved sources.
   - Live execution stage trace logs without exposing API keys, personal PII, or hidden reasoning.

## Running the Application

### 1. Backend Setup

```powershell
cd backend
# Optional: create or activate virtual environment
# py -m venv venv; .\venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt

# Run backend server
py -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Backend health check: `http://127.0.0.1:8000/health`
Interactive Swagger API docs: `http://127.0.0.1:8000/docs`

### 2. Frontend Setup

```powershell
cd frontend
npm install
npm run dev
```

Frontend application runs at: `http://localhost:3000`

### 3. Environment Variables

Configure in `backend/.env`:
- `SERPAPI_API_KEY`: Your SerpApi API key (if blank, mock search provider is used for offline tests).
- `RESEARCH_MAX_ITERATIONS`: Maximum feedback loop iterations (default: 3).
- `RESEARCH_MAX_SEARCH_BUDGET`: Maximum search queries per run (default: 5).
- `AI_PROVIDER`: `mock` (deterministic, test-friendly) or `ollama` / `openai`.

### 4. Running Backend Tests

```powershell
cd backend
py -m pytest -v
```
All 26 automated unit and integration tests execute with 100% pass rate using mocked tools and fixtures.
