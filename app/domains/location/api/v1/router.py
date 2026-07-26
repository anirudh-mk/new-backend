from fastapi import APIRouter

from .country import router as country_router
from .district import router as district_router
from .state import router as state_router

router = APIRouter()

router.include_router(country_router)
router.include_router(state_router)
router.include_router(district_router)
