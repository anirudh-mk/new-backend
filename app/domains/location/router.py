from fastapi import APIRouter

from app.domains.location.api.router import router as api_router

router = APIRouter()

router.include_router(api_router)