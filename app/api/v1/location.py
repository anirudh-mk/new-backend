from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schema.location import (
    CreateLocationRequestSchema,
    CreateLocationResponseSchema,
)
from app.service.location_service import CountryService

router = APIRouter()


@router.post(
    "/country",
    response_model=CreateLocationResponseSchema,
    status_code=201,
)
async def create_country(
        body: CreateLocationRequestSchema,
        db: AsyncSession = Depends(get_db),
):
    return await CountryService.create(db, body)
