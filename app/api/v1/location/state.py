from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schema.location.state import (
    CreateStateRequestSchema,
    StateResponseSchema,
    UpdateStateRequestSchema,
)
from app.service.location_service import StateService

router = APIRouter(
    prefix="/states",
    tags=["States"],
)


@router.get("", response_model=list[StateResponseSchema])
async def list_states(
        country_id: UUID | None = Query(
            None,
            description="Filter states by country UUID.",
        ),
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        db: AsyncSession = Depends(get_db),
):
    """
    Retrieve a paginated list of states.

    Optionally filter states by country.

    Args:
        country_id: Optional country UUID.
        skip: Number of records to skip.
        limit: Maximum number of records to return.
        db: Database session.

    Returns:
        List of states.
    """
    return await StateService.list(
        db=db,
        country_id=country_id,
        skip=skip,
        limit=limit,
    )


@router.get("/{state_id}", response_model=StateResponseSchema)
async def get_state(
        state_id: UUID,
        db: AsyncSession = Depends(get_db),
):
    """
    Retrieve a state by its unique identifier.

    Args:
        state_id: State UUID.
        db: Database session.

    Returns:
        State details.
    """
    return await StateService.get(
        db=db,
        state_id=state_id,
    )


@router.post(
    "",
    response_model=StateResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_state(
        body: CreateStateRequestSchema,
        db: AsyncSession = Depends(get_db),
):
    """
    Create a new state.

    Args:
        body: State creation request payload.
        db: Database session.

    Returns:
        The newly created state.
    """
    return await StateService.create(
        db=db,
        body=body,
    )


@router.patch("/{state_id}", response_model=StateResponseSchema)
async def update_state(
        state_id: UUID,
        body: UpdateStateRequestSchema,
        db: AsyncSession = Depends(get_db),
):
    """
    Partially update an existing state.

    Args:
        state_id: State UUID.
        body: Fields to update.
        db: Database session.

    Returns:
        The updated state.
    """
    return await StateService.patch(
        db=db,
        state_id=state_id,
        body=body,
    )


@router.delete(
    "/{state_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_state(
        state_id: UUID,
        db: AsyncSession = Depends(get_db),
):
    """
    Delete a state.

    Args:
        state_id: State UUID.
        db: Database session.

    Returns:
        None.
    """
    await StateService.delete(
        db=db,
        state_id=state_id,
    )
