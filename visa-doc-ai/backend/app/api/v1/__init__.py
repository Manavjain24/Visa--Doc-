from app.api.v1.profiles import router as profiles_router
from app.api.v1.research import router as research_router
from app.api.v1.verification import router as verification_router
from app.api.v1.checklists import router as checklists_router
from app.api.v1.requirements import router as requirements_router
from app.api.v1.sources import router as sources_router

__all__ = [
    "profiles_router",
    "research_router",
    "verification_router",
    "checklists_router",
    "requirements_router",
    "sources_router",
]
