from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CreateDistrictRequestSchema(BaseModel):
    """
    Request schema for creating a new district.

    Attributes:
        state_id: UUID of the state to which the district belongs.
        name: Name of the district.
    """

    state_id: UUID

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="District name.",
        examples=["Kozhikode"],
    )

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        """
        Normalize the district name.
        """
        return " ".join(value.strip().title().split())


class UpdateDistrictRequestSchema(BaseModel):
    """
    Request schema for partially updating a district.

    All fields are optional to support PATCH operations.
    """

    state_id: UUID | None = Field(
        None,
        description="UUID of the state to which the district belongs.",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )

    name: str | None = Field(
        None,
        min_length=1,
        max_length=100,
        description="District name.",
        examples=["Kozhikode"],
    )

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str | None) -> str | None:
        """
        Normalize the district name by trimming whitespace and
        converting it to title case.
        """
        return " ".join(value.strip().title().split()) if value else value


class DistrictResponseSchema(BaseModel):
    """
    Response schema representing a district.
    """

    id: UUID = Field(
        description="Unique identifier of the district.",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )

    state_id: UUID = Field(
        description="UUID of the state to which the district belongs.",
        examples=["550e8400-e29b-41d4-a716-446655440001"],
    )

    name: str = Field(
        description="District name.",
        examples=["Kozhikode"],
    )

    is_active: bool = Field(
        description="Indicates whether the district is active.",
        examples=[True],
    )

    created_at: datetime = Field(
        description="Timestamp when the district was created.",
    )

    updated_at: datetime = Field(
        description="Timestamp when the district was last updated.",
    )

    model_config = ConfigDict(from_attributes=True)


class ListDistrictRequestSchema(BaseModel):
    """
    Request schema for retrieving a paginated list of districts.
    """

    state_id: UUID | None = Field(
        None,
        description="Filter districts by state UUID.",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )

    search: str | None = Field(
        None,
        min_length=1,
        max_length=100,
        description="Search districts by name.",
        examples=["Koz"],
    )

    skip: int = Field(
        0,
        ge=0,
        description="Number of records to skip.",
        examples=[0],
    )

    limit: int = Field(
        100,
        ge=1,
        le=100,
        description="Maximum number of records to return.",
        examples=[100],
    )
