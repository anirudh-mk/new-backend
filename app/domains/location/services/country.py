from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.location import Country
from app.domains.location.repositories.country import (
    CountryRepository,
)
from app.domains.location.schemas.country import (
    CreateCountryRequestSchema,
    UpdateCountryRequestSchema,
)


class CountryService:
    """
    Service layer for country-related business logic.

    Handles validation, business rules, and coordinates repository operations.
    """

    @staticmethod
    async def create(db: AsyncSession, body: CreateCountryRequestSchema) -> Country:
        """
        Create a new country.

        Args:
            db: Database session.
            body: Country creation request data.

        Returns:
            The newly created country.

        Raises:
            HTTPException:
                - 409 if a country with the same Name, ISO2, or ISO3 already exists.
                - 500 if a database error occurs.
        """

        country = Country(**body.model_dump())

        try:
            return await CountryRepository.create(db, country)

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

    @staticmethod
    async def get(db: AsyncSession, country_id: UUID) -> Country:
        """
        Retrieve a country by its unique identifier.

        Args:
            db: Database session.
            country_id: Country UUID.

        Returns:
            The requested country.

        Raises:
            HTTPException:
                - 404 if the country does not exist.
                - 500 if a database error occurs.
        """

        try:
            country = await CountryRepository.get_by_id(db, country_id)

            if not country:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Country not found.",
                )

            return country

        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve country.",
            )

    @staticmethod
    async def list(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Country]:
        """
        Retrieve a paginated list of countries.

        Args:
            db: Database session.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            A list of countries.

        Raises:
            HTTPException:
                - 500 if a database error occurs.
        """

        try:
            return await CountryRepository.get_all(db=db, skip=skip, limit=limit)

        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve countries.",
            )

    @staticmethod
    async def patch(db: AsyncSession, country_id: UUID, body: UpdateCountryRequestSchema) -> Country:
        """
        Partially update an existing country.

        Args:
            db: Database session.
            country_id: Country UUID.
            body: Fields to update.

        Returns:
            The updated country.

        Raises:
            HTTPException:
                - 404 if the country does not exist.
                - 409 if a duplicate Name, ISO2, or ISO3 exists.
                - 500 if a database error occurs.
        """

        try:
            country = await CountryRepository.get_by_id(db, country_id)

            if not country:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Country not found.",
                )

            update_data = body.model_dump(exclude_unset=True)

            for field, value in update_data.items():
                setattr(country, field, value)

            return await CountryRepository.update(db, country)

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Country with the same Name, ISO2 or ISO3 already exists.",
            )

        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update country.",
            )

    @staticmethod
    async def delete(db: AsyncSession, country_id: UUID, ) -> None:
        """
         Delete a country.

         Args:
             db: Database session.
             country_id: Country UUID.

         Returns:
             None.

         Raises:
             HTTPException:
                 - 404 if the country does not exist.
                 - 500 if a database error occurs.
         """

        try:
            country = await CountryRepository.get_by_id(db, country_id)

            if not country:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Country not found.",
                )

            await CountryRepository.delete(db, country)

        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete country.",
            )
