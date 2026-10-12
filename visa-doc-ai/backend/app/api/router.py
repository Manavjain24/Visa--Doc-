from fastapi import APIRouter
from app.api.v1 import (
    profiles_router,
    research_router,
    verification_router,
    checklists_router,
    requirements_router,
    sources_router,
)

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(profiles_router)
api_router.include_router(research_router)
api_router.include_router(verification_router)
api_router.include_router(checklists_router)
api_router.include_router(requirements_router)
api_router.include_router(sources_router)
