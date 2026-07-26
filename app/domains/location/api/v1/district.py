from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.domains.location.schemas.district import (
    CreateDistrictRequestSchema,
    DistrictResponseSchema,
    UpdateDistrictRequestSchema, ListDistrictRequestSchema,
)
from app.domains.location.services.district import DistrictService

router = APIRouter(
    prefix="/districts",
    tags=["Districts"],
)


@router.get("", response_model=list[DistrictResponseSchema])
async def list_districts(
        query: ListDistrictRequestSchema = Depends(),
        db: AsyncSession = Depends(get_db),
):
    """
    Retrieve a paginated list of districts.

    Optionally filter districts by state and search by name.

    Args:
        query: District list request parameters.
        db: Database session.

    Returns:
        List of districts.
    """
    return await DistrictService.list(
        db=db,
        state_id=query.state_id,
        search=query.search,
        skip=query.skip,
        limit=query.limit,
    )


@router.get("/{district_id}", response_model=DistrictResponseSchema)
async def get_district(
        district_id: UUID,
        db: AsyncSession = Depends(get_db),
):
    """
    Retrieve a district by its unique identifier.

    Args:
        district_id: District UUID.
        db: Database session.

    Returns:
        District details.
    """
    return await DistrictService.get(
        db=db,
        district_id=district_id,
    )


@router.post(
    "",
    response_model=DistrictResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_district(
        body: CreateDistrictRequestSchema,
        db: AsyncSession = Depends(get_db),
):
    """
    Create a new district.

    Args:
        body: District creation request payload.
        db: Database session.

    Returns:
        The newly created district.
    """
    return await DistrictService.create(
        db=db,
        body=body,
    )


@router.patch("/{district_id}", response_model=DistrictResponseSchema)
async def update_district(
        district_id: UUID,
        body: UpdateDistrictRequestSchema,
        db: AsyncSession = Depends(get_db),
):
    """
    Partially update an existing district.

    Args:
        district_id: District UUID.
        body: Fields to update.
        db: Database session.

    Returns:
        The updated district.
    """
    return await DistrictService.patch(
        db=db,
        district_id=district_id,
        body=body,
    )


@router.delete(
    "/{district_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_district(
        district_id: UUID,
        db: AsyncSession = Depends(get_db),
):
    """
    Delete a district.

    Args:
        district_id: District UUID.
        db: Database session.

    Returns:
        None.
    """
    await DistrictService.delete(
        db=db,
        district_id=district_id,
    )
