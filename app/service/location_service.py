from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.location import Country
from app.repositories.location_repositories import CountryRepository
from app.schema.location import (
    CreateLocationRequestSchema,
    CreateLocationResponseSchema,
)


class CountryService:

    @staticmethod
    async def create(
            db: AsyncSession,
            body: CreateLocationRequestSchema,
    ) -> CreateLocationResponseSchema:

        country = Country(**body.model_dump())

        try:
            country = await CountryRepository.create(db, country)

            return CreateLocationResponseSchema(
                message="Country created successfully.",
                country_id=country.id,
            )

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Country with the same Name, ISO2 or ISO3 already exists.",
            )

        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create country due to a database error.",
            )
