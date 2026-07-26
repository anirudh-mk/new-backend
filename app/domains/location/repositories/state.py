from typing import List, cast
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.location import State


class StateRepository:
    """
    Repository layer for State database operations.

    Encapsulates all database interactions related to the State model.
    """

    @staticmethod
    async def create(db: AsyncSession, state: State) -> State:
        """
        Persist a new state to the database.

        Args:
            db: Active database session.
            state: State entity to be created.

        Returns:
            The newly created state with generated values populated.

        Raises:
            SQLAlchemyError: If the database operation fails.
        """
        try:
            db.add(state)
            await db.commit()
            await db.refresh(state)
            return state

        except SQLAlchemyError:
            await db.rollback()
            raise

    @staticmethod
    async def update(db: AsyncSession, state: State) -> State:
        """
        Persist changes made to an existing state.

        Args:
            db: Active database session.
            state: Existing state entity with updated values.

        Returns:
            The updated state.

        Raises:
            SQLAlchemyError: If the database operation fails.
        """
        try:
            await db.commit()
            await db.refresh(state)
            return state

        except SQLAlchemyError:
            await db.rollback()
            raise

    @staticmethod
    async def delete(db: AsyncSession, state: State) -> None:
        """
        Delete an existing state from the database.

        Args:
            db: Active database session.
            state: State entity to delete.

        Raises:
            SQLAlchemyError: If the database operation fails.
        """
        try:
            await db.delete(state)
            await db.commit()

        except SQLAlchemyError:
            await db.rollback()
            raise

    @staticmethod
    async def get_by_id(
            db: AsyncSession,
            state_id: UUID,
    ) -> State | None:
        """
        Retrieve a state by its unique identifier.

        Args:
            db: Active database session.
            state_id: State UUID.

        Returns:
            The matching state if found; otherwise, None.
        """
        result = await db.execute(
            select(State).where(State.id == state_id)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(
            db: AsyncSession,
            skip: int = 0,
            limit: int = 100,
    ) -> List[State]:
        """
        Retrieve a paginated list of states.

        States are ordered alphabetically by name.

        Args:
            db: Active database session.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            A list of states.
        """
        result = await db.execute(
            select(State)
            .order_by(State.name)
            .offset(skip)
            .limit(limit)
        )

        return cast(list[State], result.scalars().all())

    @staticmethod
    async def get_by_country_id(
            db: AsyncSession,
            country_id: UUID,
            skip: int = 0,
            limit: int = 100,
    ) -> List[State]:
        """
        Retrieve a paginated list of states belonging to a country.

        States are ordered alphabetically by name.

        Args:
            db: Active database session.
            country_id: UUID of the country.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            A list of states belonging to the specified country.
        """
        result = await db.execute(
            select(State)
            .where(State.country_id == country_id)
            .order_by(State.name)
            .offset(skip)
            .limit(limit)
        )

        return cast(list[State], result.scalars().all())
