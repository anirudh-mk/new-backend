from typing import List, cast
from uuid import UUID

from sqlalchemy import select, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.core.country import Country


class CountryRepository:
    """
    Repository layer for Country database operations.

    Encapsulates all database interactions related to the Country model.
    """

    @staticmethod
    async def create(db: AsyncSession, country: Country) -> Country:
        """
        Persist a new country to the database.

        Args:
            db: Active database session.
            country: Country entity to be created.

        Returns:
            The newly created country with generated values populated.

        Raises:
            SQLAlchemyError: If the database operation fails.
        """
        try:
            db.add(country)
            await db.commit()
            await db.refresh(country)
            return country

        except SQLAlchemyError:
            await db.rollback()
            raise

    @staticmethod
    async def update(db: AsyncSession, country: Country) -> Country:
        """
        Persist changes made to an existing country.

        Args:
            db: Active database session.
            country: Existing country entity with updated values.

        Returns:
            The updated country.

        Raises:
            SQLAlchemyError: If the database operation fails.
        """
        try:
            await db.commit()
            await db.refresh(country)
            return country

        except SQLAlchemyError:
            await db.rollback()
            raise

    @staticmethod
    async def delete(db: AsyncSession, country: Country) -> None:
        """
        Delete an existing country from the database.

        Args:
            db: Active database session.
            country: Country entity to delete.

        Raises:
            SQLAlchemyError: If the database operation fails.
        """
        try:
            await db.delete(country)
            await db.commit()

        except SQLAlchemyError:
            await db.rollback()
            raise

    @staticmethod
    async def get_by_id(
            db: AsyncSession,
            country_id: UUID,
    ) -> Country | None:
        """
        Retrieve a country by its unique identifier.

        Args:
            db: Active database session.
            country_id: Country UUID.

        Returns:
            The matching country if found; otherwise, None.
        """
        result = await db.execute(
            select(Country).where(Country.id == country_id)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(
            db: AsyncSession,
            search: str | None = None,
            skip: int = 0,
            limit: int = 100,
    ) -> List[Country]:
        """
        Retrieve a paginated list of countries.

        Optionally filter countries by name, ISO2 code, ISO3 code,
        phone code, or currency code. Results are ordered
        alphabetically by country name.

        Args:
            db: Active database session.
            search: Optional search term used to match the country name,
                ISO2 code, ISO3 code, phone code, or currency code.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            A list of countries.
        """
        query = select(Country)

        if search:
            search = search.strip()

            query = query.where(
                or_(
                    Country.name.ilike(f"%{search}%"),
                    Country.iso2.ilike(f"%{search}%"),
                    Country.iso3.ilike(f"%{search}%"),
                    Country.phone_code.ilike(f"%{search}%"),
                    Country.currency_code.ilike(f"%{search}%"),
                )
            )

        result = await db.execute(
            query
            .order_by(Country.name)
            .offset(skip)
            .limit(limit)
        )

        return cast(list[Country], result.scalars().all())
