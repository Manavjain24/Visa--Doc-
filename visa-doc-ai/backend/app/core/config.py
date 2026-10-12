import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # SerpApi Configuration
    SERPAPI_API_KEY: str = ""
    SERPAPI_MAX_RESULTS: int = 8
    SERPAPI_TIMEOUT_SECONDS: float = 10.0
    SERPAPI_MAX_RETRIES: int = 2

    # Agentic Research Constraints
    RESEARCH_MAX_ITERATIONS: int = 3
    RESEARCH_MAX_SEARCH_BUDGET: int = 5

    # Ingestion Security & Limits
    INGESTION_TIMEOUT_SECONDS: float = 10.0
    INGESTION_MAX_CONTENT_LENGTH: int = 150000
    INGESTION_USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) VisaDocAI/1.0"

    # Database
    DATABASE_URL: str = "sqlite:///./visadoc.db"

    # AI Configuration
    AI_PROVIDER: str = "mock"  # mock, ollama, openai, gemini
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
