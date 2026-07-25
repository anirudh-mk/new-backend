from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.location import Country


class CountryRepository:

    @staticmethod
    async def create(db: AsyncSession, country: Country) -> Country:
        try:
            db.add(country)

            await db.commit()

            await db.refresh(country)

            return country

        except SQLAlchemyError:
            await db.rollback()
            raise
