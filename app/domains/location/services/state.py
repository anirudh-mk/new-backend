from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.location.repositories.country import CountryRepository
from app.domains.location.repositories.state import (
    StateRepository,
)
from app.domains.location.schemas.state import (
    CreateStateRequestSchema,
    UpdateStateRequestSchema,
)
from app.models.core.state import State


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
            search: str | None = None,
            skip: int = 0,
            limit: int = 100,
    ) -> List[State]:
        """
        Retrieve a paginated list of states.

        Optionally filter states by country and search by name or code.

        Args:
            db: Database session.
            country_id: Optional country UUID used to filter states.
            search: Optional search term used to match the state name
                or code.
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
                    search=search,
                    skip=skip,
                    limit=limit,
                )

            return await StateRepository.get_all(
                db=db,
                search=search,
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
