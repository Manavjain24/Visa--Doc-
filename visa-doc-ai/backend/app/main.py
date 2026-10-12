from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import logger
from app.db.init_db import init_db
from app.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database schema...")
    init_db()
    logger.info("VisaDoc AI backend startup complete.")
    yield
    logger.info("VisaDoc AI backend shutting down.")


app = FastAPI(
    title="VisaDoc AI API",
    description="Evidence-grounded, bounded agentic visa research and verification system",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if settings.CORS_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health", tags=["Health"])
@app.get("/api/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "visadoc-ai-backend",
        "environment": settings.ENVIRONMENT,
        "serpapi_configured": bool(settings.SERPAPI_API_KEY),
        "ai_provider": settings.AI_PROVIDER,
        "max_iterations": settings.RESEARCH_MAX_ITERATIONS,
        "search_budget": settings.RESEARCH_MAX_SEARCH_BUDGET,
    }
