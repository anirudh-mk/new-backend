from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.location.repositories.district import DistrictRepository
from app.domains.location.repositories.state import StateRepository
from app.domains.location.schemas.district import (
    CreateDistrictRequestSchema,
    UpdateDistrictRequestSchema,
)
from app.models.location import District


class DistrictService:
    """
    Service layer for district-related business logic.

    Handles validation, business rules, and coordinates repository operations.
    """

    @staticmethod
    async def create(
            db: AsyncSession,
            body: CreateDistrictRequestSchema,
    ) -> District:
        """
        Create a new district.

        Args:
            db: Database session.
            body: District creation request data.

        Returns:
            The newly created district.

        Raises:
            HTTPException:
                - 404 if the specified state does not exist.
                - 409 if a district with the same name already exists for the state.
                - 500 if a database error occurs.
        """

        try:
            state = await StateRepository.get_by_id(db, body.state_id)

            if not state:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="State not found.",
                )

            district = District(**body.model_dump())

            return await DistrictRepository.create(db, district)

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="District with the same name already exists for this state.",
            )

        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create district due to a database error.",
            )

    @staticmethod
    async def get(
            db: AsyncSession,
            district_id: UUID,
    ) -> District:
        """
        Retrieve a district by its unique identifier.

        Args:
            db: Database session.
            district_id: District UUID.

        Returns:
            The requested district.

        Raises:
            HTTPException:
                - 404 if the district does not exist.
                - 500 if a database error occurs.
        """

        try:
            district = await DistrictRepository.get_by_id(db, district_id)

            if not district:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="District not found.",
                )

            return district

        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve district.",
            )

    @staticmethod
    async def list(
            db: AsyncSession,
            state_id: UUID | None = None,
            skip: int = 0,
            limit: int = 100,
    ) -> List[District]:
        """
        Retrieve a paginated list of districts.

        If a state ID is provided, only districts belonging to that state
        are returned.

        Args:
            db: Database session.
            state_id: Optional state UUID.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            A list of districts.

        Raises:
            HTTPException:
                - 404 if the provided state does not exist.
                - 500 if a database error occurs.
        """

        try:
            if state_id is not None:
                state = await StateRepository.get_by_id(db, state_id)

                if not state:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="State not found.",
                    )

                return await DistrictRepository.get_by_state_id(
                    db=db,
                    state_id=state_id,
                    skip=skip,
                    limit=limit,
                )

            return await DistrictRepository.get_all(
                db=db,
                skip=skip,
                limit=limit,
            )

        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve districts.",
            )

    @staticmethod
    async def patch(
            db: AsyncSession,
            district_id: UUID,
            body: UpdateDistrictRequestSchema,
    ) -> District:
        """
        Partially update an existing district.

        Args:
            db: Database session.
            district_id: District UUID.
            body: Fields to update.

        Returns:
            The updated district.

        Raises:
            HTTPException:
                - 404 if the district or state does not exist.
                - 409 if a duplicate district exists.
                - 500 if a database error occurs.
        """

        try:
            district = await DistrictRepository.get_by_id(
                db,
                district_id,
            )

            if not district:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="District not found.",
                )

            update_data = body.model_dump(exclude_unset=True)

            if "state_id" in update_data:
                state = await StateRepository.get_by_id(
                    db,
                    update_data["state_id"],
                )

                if not state:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="State not found.",
                    )

            for field, value in update_data.items():
                setattr(district, field, value)

            return await DistrictRepository.update(db, district)

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="District with the same name already exists for this state.",
            )

        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update district.",
            )

    @staticmethod
    async def delete(
            db: AsyncSession,
            district_id: UUID,
    ) -> None:
        """
        Delete a district.

        Args:
            db: Database session.
            district_id: District UUID.

        Returns:
            None.

        Raises:
            HTTPException:
                - 404 if the district does not exist.
                - 500 if a database error occurs.
        """

        try:
            district = await DistrictRepository.get_by_id(
                db,
                district_id,
            )

            if not district:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="District not found.",
                )

            await DistrictRepository.delete(db, district)

        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete district.",
            )
