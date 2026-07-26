from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CreateCountryRequestSchema(BaseModel):
    """
    Request schema for creating a new country.
    """

    name: str = Field(..., min_length=1, max_length=100)
    iso2: str = Field(..., min_length=2, max_length=2)
    iso3: str = Field(..., min_length=3, max_length=3)
    phone_code: str = Field(..., min_length=1, max_length=5)
    currency_code: str = Field(..., min_length=3, max_length=3)

    @field_validator("iso2", "iso3", "currency_code")
    @classmethod
    def uppercase(cls, value: str) -> str:
        """
        Convert ISO and currency codes to uppercase.

        Args:
            value: Input field value.

        Returns:
            Uppercase representation of the value.
        """
        return value.upper()


class CountryResponseSchema(BaseModel):
    """
    Response schema representing a country.
    """

    id: UUID
    name: str
    iso2: str
    iso3: str
    phone_code: str
    currency_code: str

    model_config = ConfigDict(from_attributes=True)


class UpdateCountryRequestSchema(BaseModel):
    """
    Request schema for partially updating a country.

    All fields are optional to support PATCH operations.
    """

    name: str | None = Field(None, min_length=1, max_length=100)
    iso2: str | None = Field(None, min_length=2, max_length=2)
    iso3: str | None = Field(None, min_length=3, max_length=3)
    phone_code: str | None = Field(None, min_length=1, max_length=5)
    currency_code: str | None = Field(None, min_length=3, max_length=3)

    @field_validator("iso2", "iso3", "currency_code")
    @classmethod
    def uppercase(cls, value: str | None) -> str | None:
        """
        Convert ISO and currency codes to uppercase when provided.

        Args:
            value: Input field value.

        Returns:
            Uppercase representation of the value, or None.
        """
        return value.upper() if value else value
