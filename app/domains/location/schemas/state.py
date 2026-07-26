from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CreateStateRequestSchema(BaseModel):
    """
    Request schemas for creating a new state.

    Attributes:
        country_id: UUID of the country to which the state belongs.
        name: Name of the state.
        code: Optional short code or abbreviation for the state.
    """

    country_id: UUID

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="State name.",
        examples=["Kerala"],
    )

    code: str | None = Field(
        None,
        min_length=1,
        max_length=10,
        description="Optional state code.",
        examples=["KL"],
    )

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        """
        Normalize the state name.
        """
        return " ".join(value.strip().title().split())

    @field_validator("code")
    @classmethod
    def normalize_code(cls, value: str | None) -> str | None:
        """
        Normalize the state code to uppercase.
        """
        return value.strip().upper() if value else value


class UpdateStateRequestSchema(BaseModel):
    """
    Request schemas for partially updating a state.

    All fields are optional to support PATCH operations.
    """

    country_id: UUID | None = Field(
        None,
        description="UUID of the country to which the state belongs.",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )

    name: str | None = Field(
        None,
        min_length=1,
        max_length=100,
        description="State name.",
        examples=["Kerala"],
    )

    code: str | None = Field(
        None,
        min_length=1,
        max_length=10,
        description="Optional state code.",
        examples=["KL"],
    )

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str | None) -> str | None:
        """
        Normalize the state name by trimming whitespace and
        converting it to title case.
        """
        return " ".join(value.strip().title().split()) if value else value

    @field_validator("code")
    @classmethod
    def normalize_code(cls, value: str | None) -> str | None:
        """
        Normalize the state code to uppercase.
        """
        return value.strip().upper() if value else value


class StateResponseSchema(BaseModel):
    """
    Response schemas representing a state.
    """

    id: UUID = Field(
        description="Unique identifier of the state.",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )

    country_id: UUID = Field(
        description="UUID of the country to which the state belongs.",
        examples=["550e8400-e29b-41d4-a716-446655440001"],
    )

    name: str = Field(
        description="State name.",
        examples=["Kerala"],
    )

    code: str | None = Field(
        description="Optional state code.",
        examples=["KL"],
    )

    is_active: bool = Field(
        description="Indicates whether the state is active.",
        examples=[True],
    )

    created_at: datetime = Field(
        description="Timestamp when the state was created.",
    )

    updated_at: datetime = Field(
        description="Timestamp when the state was last updated.",
    )

    model_config = ConfigDict(from_attributes=True)


class ListStateRequestSchema(BaseModel):
    """
    Request schema for retrieving a paginated list of states.
    """

    country_id: UUID | None = Field(
        None,
        description="Filter states by country UUID.",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )

    search: str | None = Field(
        None,
        min_length=1,
        max_length=100,
        description="Search states by name.",
        examples=["Ker"],
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
