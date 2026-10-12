visa-doc-ai/
│
├── frontend/
│   ├── public/
│   │   ├── images/
│   │   │   └── logo.svg
│   │   └── favicon.ico
│   │
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   ├── globals.css
│   │   │   ├── not-found.tsx
│   │   │   ├── error.tsx
│   │   │   ├── loading.tsx
│   │   │   │
│   │   │   ├── visa-profile/
│   │   │   │   └── page.tsx
│   │   │   │
│   │   │   ├── research/
│   │   │   │   └── [runId]/
│   │   │   │       └── page.tsx
│   │   │   │
│   │   │   ├── checklist/
│   │   │   │   └── [checklistId]/
│   │   │   │       └── page.tsx
│   │   │   │
│   │   │   ├── verify/
│   │   │   │   └── page.tsx
│   │   │   │
│   │   │   └── sources/
│   │   │       └── [sourceId]/
│   │   │           └── page.tsx
│   │   │
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── navbar.tsx
│   │   │   │   ├── footer.tsx
│   │   │   │   └── page-container.tsx
│   │   │   │
│   │   │   ├── profile/
│   │   │   │   ├── visa-profile-form.tsx
│   │   │   │   └── profile-summary.tsx
│   │   │   │
│   │   │   ├── research/
│   │   │   │   ├── research-progress.tsx
│   │   │   │   ├── search-result-card.tsx
│   │   │   │   └── source-list.tsx
│   │   │   │
│   │   │   ├── requirements/
│   │   │   │   ├── requirement-card.tsx
│   │   │   │   ├── requirement-badge.tsx
│   │   │   │   ├── evidence-panel.tsx
│   │   │   │   └── conflict-panel.tsx
│   │   │   │
│   │   │   ├── checklist/
│   │   │   │   ├── checklist-view.tsx
│   │   │   │   ├── checklist-item.tsx
│   │   │   │   └── checklist-filters.tsx
│   │   │   │
│   │   │   ├── verification/
│   │   │   │   ├── claim-form.tsx
│   │   │   │   └── verification-result.tsx
│   │   │   │
│   │   │   └── ui/
│   │   │       ├── button.tsx
│   │   │       ├── input.tsx
│   │   │       ├── select.tsx
│   │   │       ├── badge.tsx
│   │   │       └── alert.tsx
│   │   │
│   │   ├── lib/
│   │   │   ├── api-client.ts
│   │   │   ├── utils.ts
│   │   │   ├── constants.ts
│   │   │   └── validations/
│   │   │       ├── visa-profile.ts
│   │   │       └── claim.ts
│   │   │
│   │   ├── hooks/
│   │   │   ├── use-visa-profile.ts
│   │   │   ├── use-research.ts
│   │   │   └── use-checklist.ts
│   │   │
│   │   └── types/
│   │       ├── visa.ts
│   │       ├── research.ts
│   │       ├── requirement.ts
│   │       └── checklist.ts
│   │
│   ├── .env.local.example
│   ├── .env.local
│   ├── .gitignore
│   ├── eslint.config.mjs
│   ├── next.config.ts
│   ├── next-env.d.ts
│   ├── package.json
│   ├── package-lock.json
│   ├── postcss.config.mjs
│   ├── tsconfig.json
│   └── README.md
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── profiles.py
│   │   │       ├── research.py
│   │   │       ├── requirements.py
│   │   │       ├── verification.py
│   │   │       ├── checklists.py
│   │   │       └── sources.py
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── logging.py
│   │   │   ├── exceptions.py
│   │   │   └── security.py
│   │   │
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── session.py
│   │   │   ├── base.py
│   │   │   └── init_db.py
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── visa_profile.py
│   │   │   ├── research_run.py
│   │   │   ├── source.py
│   │   │   ├── requirement.py
│   │   │   ├── evidence.py
│   │   │   └── checklist.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── common.py
│   │   │   ├── visa_profile.py
│   │   │   ├── research.py
│   │   │   ├── search.py
│   │   │   ├── source.py
│   │   │   ├── requirement.py
│   │   │   ├── verification.py
│   │   │   └── checklist.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── research_service.py
│   │   │   ├── profile_service.py
│   │   │   ├── requirement_service.py
│   │   │   ├── verification_service.py
│   │   │   └── checklist_service.py
│   │   │
│   │   ├── search/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── serpapi_provider.py
│   │   │   ├── query_builder.py
│   │   │   ├── result_normalizer.py
│   │   │   └── cache.py
│   │   │
│   │   ├── ingestion/
│   │   │   ├── __init__.py
│   │   │   ├── url_validator.py
│   │   │   ├── page_fetcher.py
│   │   │   ├── content_extractor.py
│   │   │   └── pdf_extractor.py
│   │   │
│   │   ├── verification/
│   │   │   ├── __init__.py
│   │   │   ├── requirement_extractor.py
│   │   │   ├── classifier.py
│   │   │   ├── evidence_validator.py
│   │   │   ├── source_ranker.py
│   │   │   └── conflict_detector.py
│   │   │
│   │   ├── ai/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── ollama_provider.py
│   │   │   └── prompts.py
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── url_utils.py
│   │       └── text_utils.py
│   │
│   ├── alembic/
│   │   ├── versions/
│   │   │   └── .gitkeep
│   │   ├── env.py
│   │   └── script.py.mako
│   │
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── fixtures/
│   │   │   ├── search_results.json
│   │   │   └── sample_official_page.html
│   │   ├── test_health.py
│   │   ├── test_profiles.py
│   │   ├── test_serpapi_provider.py
│   │   ├── test_query_builder.py
│   │   ├── test_content_extractor.py
│   │   ├── test_requirement_classifier.py
│   │   ├── test_evidence_validator.py
│   │   ├── test_conflict_detector.py
│   │   ├── test_verification.py
│   │   └── test_checklists.py
│   │
│   ├── .env.example
│   ├── .gitignore
│   ├── alembic.ini
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── README.md
│
├── docs/
│   ├── architecture.md
│   ├── api-specification.md
│   ├── database-schema.md
│   ├── verification-policy.md
│   ├── serpapi-integration.md
│   ├── security-and-privacy.md
│   ├── testing.md
│   └── demo-script.md
│
├── scripts/
│   ├── setup.ps1
│   ├── dev.ps1
│   └── check-env.ps1
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile.backend
├── Dockerfile.frontend
├── compose.yaml
├── Makefile
├── LICENSE
└── README.mdvisa-doc-ai/
│
├── frontend/
│   ├── public/
│   │   ├── images/
│   │   │   └── logo.svg
│   │   └── favicon.ico
│   │
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   ├── globals.css
│   │   │   ├── not-found.tsx
│   │   │   ├── error.tsx
│   │   │   ├── loading.tsx
│   │   │   │
│   │   │   ├── visa-profile/
│   │   │   │   └── page.tsx
│   │   │   │
│   │   │   ├── research/
│   │   │   │   └── [runId]/
│   │   │   │       └── page.tsx
│   │   │   │
│   │   │   ├── checklist/
│   │   │   │   └── [checklistId]/
│   │   │   │       └── page.tsx
│   │   │   │
│   │   │   ├── verify/
│   │   │   │   └── page.tsx
│   │   │   │
│   │   │   └── sources/
│   │   │       └── [sourceId]/
│   │   │           └── page.tsx
│   │   │
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── navbar.tsx
│   │   │   │   ├── footer.tsx
│   │   │   │   └── page-container.tsx
│   │   │   │
│   │   │   ├── profile/
│   │   │   │   ├── visa-profile-form.tsx
│   │   │   │   └── profile-summary.tsx
│   │   │   │
│   │   │   ├── research/
│   │   │   │   ├── research-progress.tsx
│   │   │   │   ├── search-result-card.tsx
│   │   │   │   └── source-list.tsx
│   │   │   │
│   │   │   ├── requirements/
│   │   │   │   ├── requirement-card.tsx
│   │   │   │   ├── requirement-badge.tsx
│   │   │   │   ├── evidence-panel.tsx
│   │   │   │   └── conflict-panel.tsx
│   │   │   │
│   │   │   ├── checklist/
│   │   │   │   ├── checklist-view.tsx
│   │   │   │   ├── checklist-item.tsx
│   │   │   │   └── checklist-filters.tsx
│   │   │   │
│   │   │   ├── verification/
│   │   │   │   ├── claim-form.tsx
│   │   │   │   └── verification-result.tsx
│   │   │   │
│   │   │   └── ui/
│   │   │       ├── button.tsx
│   │   │       ├── input.tsx
│   │   │       ├── select.tsx
│   │   │       ├── badge.tsx
│   │   │       └── alert.tsx
│   │   │
│   │   ├── lib/
│   │   │   ├── api-client.ts
│   │   │   ├── utils.ts
│   │   │   ├── constants.ts
│   │   │   └── validations/
│   │   │       ├── visa-profile.ts
│   │   │       └── claim.ts
│   │   │
│   │   ├── hooks/
│   │   │   ├── use-visa-profile.ts
│   │   │   ├── use-research.ts
│   │   │   └── use-checklist.ts
│   │   │
│   │   └── types/
│   │       ├── visa.ts
│   │       ├── research.ts
│   │       ├── requirement.ts
│   │       └── checklist.ts
│   │
│   ├── .env.local.example
│   ├── .env.local
│   ├── .gitignore
│   ├── eslint.config.mjs
│   ├── next.config.ts
│   ├── next-env.d.ts
│   ├── package.json
│   ├── package-lock.json
│   ├── postcss.config.mjs
│   ├── tsconfig.json
│   └── README.md
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── profiles.py
│   │   │       ├── research.py
│   │   │       ├── requirements.py
│   │   │       ├── verification.py
│   │   │       ├── checklists.py
│   │   │       └── sources.py
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── logging.py
│   │   │   ├── exceptions.py
│   │   │   └── security.py
│   │   │
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── session.py
│   │   │   ├── base.py
│   │   │   └── init_db.py
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── visa_profile.py
│   │   │   ├── research_run.py
│   │   │   ├── source.py
│   │   │   ├── requirement.py
│   │   │   ├── evidence.py
│   │   │   └── checklist.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── common.py
│   │   │   ├── visa_profile.py
│   │   │   ├── research.py
│   │   │   ├── search.py
│   │   │   ├── source.py
│   │   │   ├── requirement.py
│   │   │   ├── verification.py
│   │   │   └── checklist.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── research_service.py
│   │   │   ├── profile_service.py
│   │   │   ├── requirement_service.py
│   │   │   ├── verification_service.py
│   │   │   └── checklist_service.py
│   │   │
│   │   ├── search/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── serpapi_provider.py
│   │   │   ├── query_builder.py
│   │   │   ├── result_normalizer.py
│   │   │   └── cache.py
│   │   │
│   │   ├── ingestion/
│   │   │   ├── __init__.py
│   │   │   ├── url_validator.py
│   │   │   ├── page_fetcher.py
│   │   │   ├── content_extractor.py
│   │   │   └── pdf_extractor.py
│   │   │
│   │   ├── verification/
│   │   │   ├── __init__.py
│   │   │   ├── requirement_extractor.py
│   │   │   ├── classifier.py
│   │   │   ├── evidence_validator.py
│   │   │   ├── source_ranker.py
│   │   │   └── conflict_detector.py
│   │   │
│   │   ├── ai/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── ollama_provider.py
│   │   │   └── prompts.py
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── url_utils.py
│   │       └── text_utils.py
│   │
│   ├── alembic/
│   │   ├── versions/
│   │   │   └── .gitkeep
│   │   ├── env.py
│   │   └── script.py.mako
│   │
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── fixtures/
│   │   │   ├── search_results.json
│   │   │   └── sample_official_page.html
│   │   ├── test_health.py
│   │   ├── test_profiles.py
│   │   ├── test_serpapi_provider.py
│   │   ├── test_query_builder.py
│   │   ├── test_content_extractor.py
│   │   ├── test_requirement_classifier.py
│   │   ├── test_evidence_validator.py
│   │   ├── test_conflict_detector.py
│   │   ├── test_verification.py
│   │   └── test_checklists.py
│   │
│   ├── .env.example
│   ├── .gitignore
│   ├── alembic.ini
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── README.md
│
├── docs/
│   ├── architecture.md
│   ├── api-specification.md
│   ├── database-schema.md
│   ├── verification-policy.md
│   ├── serpapi-integration.md
│   ├── security-and-privacy.md
│   ├── testing.md
│   └── demo-script.md
│
├── scripts/
│   ├── setup.ps1
│   ├── dev.ps1
│   └── check-env.ps1
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile.backend
├── Dockerfile.frontend
├── compose.yaml
├── Makefile
├── LICENSE
└── README.md