from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.location import Country
from app.models.location import State
from app.repositories.location_repositories import (
    CountryRepository,
    StateRepository,
)
from app.schema.location import (
    CreateCountryRequestSchema,
    UpdateCountryRequestSchema,
)
from app.schema.location import (
    CreateStateRequestSchema,
    UpdateStateRequestSchema,
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


class StateService:
    """
    Service layer for state-related business logic.

    Handles validation, business rules, and coordinates repository operations.
    """

    @staticmethod
    async def create(db: AsyncSession, body: CreateStateRequestSchema) -> State:
        """
        Create a new state.

        Args:
            db: Database session.
            body: State creation request data.

        Returns:
            The newly created state.

        Raises:
            HTTPException:
                - 404 if the specified country does not exist.
                - 409 if a state with the same name already exists for the country.
                - 500 if a database error occurs.
        """

        try:
            country = await CountryRepository.get_by_id(db, body.country_id)

            if not country:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Country not found.",
                )

            state = State(**body.model_dump())

            return await StateRepository.create(db, state)

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="State with the same name already exists for this country.",
            )

        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create state due to a database error.",
            )

    @staticmethod
    async def get(db: AsyncSession, state_id: UUID) -> State:
        """
        Retrieve a state by its unique identifier.

        Args:
            db: Database session.
            state_id: State UUID.

        Returns:
            The requested state.

        Raises:
            HTTPException:
                - 404 if the state does not exist.
                - 500 if a database error occurs.
        """

        try:
            state = await StateRepository.get_by_id(db, state_id)

            if not state:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="State not found.",
                )

            return state

        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve state.",
            )

    @staticmethod
    async def list(
            db: AsyncSession,
            country_id: UUID | None = None,
            skip: int = 0,
            limit: int = 100,
    ) -> List[State]:
        """
        Retrieve a paginated list of states.

        If a country ID is provided, only states belonging to that country
        are returned.

        Args:
            db: Database session.
            country_id: Optional country UUID.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            A list of states.

        Raises:
            HTTPException:
                - 404 if the provided country does not exist.
                - 500 if a database error occurs.
        """

        try:
            if country_id is not None:
                country = await CountryRepository.get_by_id(db, country_id)

                if not country:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Country not found.",
                    )

                return await StateRepository.get_by_country_id(
                    db=db,
                    country_id=country_id,
                    skip=skip,
                    limit=limit,
                )

            return await StateRepository.get_all(
                db=db,
                skip=skip,
                limit=limit,
            )

        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve states.",
            )

    @staticmethod
    async def patch(
            db: AsyncSession,
            state_id: UUID,
            body: UpdateStateRequestSchema,
    ) -> State:
        """
        Partially update an existing state.

        Args:
            db: Database session.
            state_id: State UUID.
            body: Fields to update.

        Returns:
            The updated state.

        Raises:
            HTTPException:
                - 404 if the state or country does not exist.
                - 409 if a duplicate state exists.
                - 500 if a database error occurs.
        """

        try:
            state = await StateRepository.get_by_id(db, state_id)

            if not state:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="State not found.",
                )

            update_data = body.model_dump(exclude_unset=True)

            if "country_id" in update_data:
                country = await CountryRepository.get_by_id(
                    db,
                    update_data["country_id"],
                )

                if not country:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Country not found.",
                    )

            for field, value in update_data.items():
                setattr(state, field, value)

            return await StateRepository.update(db, state)

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="State with the same name already exists for this country.",
            )

        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update state.",
            )

    @staticmethod
    async def delete(
            db: AsyncSession,
            state_id: UUID,
    ) -> None:
        """
        Delete a state.

        Args:
            db: Database session.
            state_id: State UUID.

        Returns:
            None.

        Raises:
            HTTPException:
                - 404 if the state does not exist.
                - 500 if a database error occurs.
        """

        try:
            state = await StateRepository.get_by_id(db, state_id)

            if not state:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="State not found.",
                )

            await StateRepository.delete(db, state)

        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete state.",
            )
