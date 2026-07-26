from fastapi import APIRouter

from app.domains.location.router import router as location_router

router = APIRouter(
    prefix="/api",
)

router.include_router(location_router)
