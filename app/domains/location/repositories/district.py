from typing import List, cast
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.location import District


class DistrictRepository:
    """
    Repository layer for District database operations.

    Encapsulates all database interactions related to the District model.
    """

    @staticmethod
    async def create(db: AsyncSession, district: District) -> District:
        """
        Persist a new district to the database.

        Args:
            db: Active database session.
            district: District entity to be created.

        Returns:
            The newly created district with generated values populated.

        Raises:
            SQLAlchemyError: If the database operation fails.
        """
        try:
            db.add(district)
            await db.commit()
            await db.refresh(district)
            return district

        except SQLAlchemyError:
            await db.rollback()
            raise

    @staticmethod
    async def update(db: AsyncSession, district: District) -> District:
        """
        Persist changes made to an existing district.

        Args:
            db: Active database session.
            district: Existing district entity with updated values.

        Returns:
            The updated district.

        Raises:
            SQLAlchemyError: If the database operation fails.
        """
        try:
            await db.commit()
            await db.refresh(district)
            return district

        except SQLAlchemyError:
            await db.rollback()
            raise

    @staticmethod
    async def delete(db: AsyncSession, district: District) -> None:
        """
        Delete an existing district from the database.

        Args:
            db: Active database session.
            district: District entity to delete.

        Raises:
            SQLAlchemyError: If the database operation fails.
        """
        try:
            await db.delete(district)
            await db.commit()

        except SQLAlchemyError:
            await db.rollback()
            raise

    @staticmethod
    async def get_by_id(
            db: AsyncSession,
            district_id: UUID,
    ) -> District | None:
        """
        Retrieve a district by its unique identifier.

        Args:
            db: Active database session.
            district_id: District UUID.

        Returns:
            The matching district if found; otherwise, None.
        """
        result = await db.execute(
            select(District).where(District.id == district_id)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(
            db: AsyncSession,
            skip: int = 0,
            limit: int = 100,
    ) -> List[District]:
        """
        Retrieve a paginated list of districts.

        Districts are ordered alphabetically by name.

        Args:
            db: Active database session.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            A list of districts.
        """
        result = await db.execute(
            select(District)
            .order_by(District.name)
            .offset(skip)
            .limit(limit)
        )

        return cast(list[District], result.scalars().all())

    @staticmethod
    async def get_by_state_id(
            db: AsyncSession,
            state_id: UUID,
            skip: int = 0,
            limit: int = 100,
    ) -> List[District]:
        """
        Retrieve a paginated list of districts belonging to a state.

        Districts are ordered alphabetically by name.

        Args:
            db: Active database session.
            state_id: UUID of the state.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            A list of districts belonging to the specified state.
        """
        result = await db.execute(
            select(District)
            .where(District.state_id == state_id)
            .order_by(District.name)
            .offset(skip)
            .limit(limit)
        )

        return cast(list[District], result.scalars().all())
