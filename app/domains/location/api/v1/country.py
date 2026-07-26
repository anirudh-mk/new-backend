from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.domains.location.schemas.country import (
    CreateCountryRequestSchema,
    CountryResponseSchema,
    UpdateCountryRequestSchema, ListCountryRequestSchema,
)
from app.domains.location.services.country import CountryService

router = APIRouter(
    prefix="/countries",
    tags=["Countries"],
)


@router.get("", response_model=list[CountryResponseSchema])
async def list_countries(
        query: ListCountryRequestSchema = Depends(),
        db: AsyncSession = Depends(get_db),
):
    """
    Retrieve a paginated list of countries.

    Optionally filter countries by name, ISO2 code, ISO3 code,
    phone code, or currency code.

    Args:
        query: Country list request parameters.
        db: Database session.

    Returns:
        List of countries.
    """
    return await CountryService.list(
        db=db,
        search=query.search,
        skip=query.skip,
        limit=query.limit,
    )


@router.get("/{country_id}", response_model=CountryResponseSchema)
async def get_country(
        country_id: UUID,
        db: AsyncSession = Depends(get_db),
):
    """
    Retrieve a country by its unique identifier.

    Args:
        country_id: Country UUID.
        db: Database session.

    Returns:
        Country details.
    """
    return await CountryService.get(
        db=db,
        country_id=country_id,
    )


@router.post(
    "",
    response_model=CountryResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_country(
        body: CreateCountryRequestSchema,
        db: AsyncSession = Depends(get_db),
):
    """
    Create a new country.

    Args:
        body: Country creation request payload.
        db: Database session.

    Returns:
        The newly created country.
    """
    return await CountryService.create(
        db,
        body,
    )


@router.patch("/{country_id}", response_model=CountryResponseSchema)
async def update_country(
        country_id: UUID,
        body: UpdateCountryRequestSchema,
        db: AsyncSession = Depends(get_db),
):
    """
    Partially update an existing country.

    Args:
        country_id: Country UUID.
        body: Fields to update.
        db: Database session.

    Returns:
        The updated country.
    """
    return await CountryService.patch(
        db=db,
        country_id=country_id,
        body=body,
    )


@router.delete(
    "/{country_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_country(
        country_id: UUID,
        db: AsyncSession = Depends(get_db),
):
    """
    Delete a country.

    Args:
        country_id: Country UUID.
        db: Database session.

    Returns:
        None.
    """
    await CountryService.delete(
        db=db,
        country_id=country_id,
    )
