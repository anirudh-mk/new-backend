from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class CreateLocationRequestSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    iso2: str = Field(..., min_length=2, max_length=2)
    iso3: str = Field(..., min_length=3, max_length=3)
    phone_code: str = Field(..., min_length=1, max_length=5)
    currency_code: str = Field(..., min_length=3, max_length=3)

    @field_validator("iso2", "iso3", "currency_code")
    @classmethod
    def uppercase(cls, value: str):
        return value.upper()


class CreateLocationResponseSchema(BaseModel):
    message: str
    country_id: UUID
