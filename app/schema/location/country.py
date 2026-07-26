from uuid import UUID

from pydantic import BaseModel, Field, field_validator
from pydantic import ConfigDict


class CreateCountryRequestSchema(BaseModel):
    """
    Request schema for creating a new country.
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Country name.",
        examples=["India"],
    )

    iso2: str = Field(
        ...,
        min_length=2,
        max_length=2,
        description="ISO 3166-1 alpha-2 country code.",
        examples=["IN"],
    )

    iso3: str = Field(
        ...,
        min_length=3,
        max_length=3,
        description="ISO 3166-1 alpha-3 country code.",
        examples=["IND"],
    )

    phone_code: str = Field(
        ...,
        min_length=1,
        max_length=5,
        description="International dialing code.",
        examples=["+91"],
    )

    currency_code: str = Field(
        ...,
        min_length=3,
        max_length=3,
        description="ISO 4217 currency code.",
        examples=["INR"],
    )

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        """
        Normalize the country name by trimming whitespace and
        converting it to title case.
        """
        return " ".join(value.strip().title().split())

    @field_validator("iso2", "iso3", "currency_code")
    @classmethod
    def normalize_codes(cls, value: str) -> str:
        """
        Normalize ISO and currency codes to uppercase.
        """
        return value.strip().upper()

    @field_validator("phone_code")
    @classmethod
    def normalize_phone_code(cls, value: str) -> str:
        """
        Remove leading and trailing whitespace from the phone code.
        """
        return value.strip()


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

    name: str | None = Field(
        None,
        min_length=1,
        max_length=100,
        description="Country name.",
        examples=["India"],
    )

    iso2: str | None = Field(
        None,
        min_length=2,
        max_length=2,
        description="ISO 3166-1 alpha-2 country code.",
        examples=["IN"],
    )

    iso3: str | None = Field(
        None,
        min_length=3,
        max_length=3,
        description="ISO 3166-1 alpha-3 country code.",
        examples=["IND"],
    )

    phone_code: str | None = Field(
        None,
        min_length=1,
        max_length=5,
        description="International dialing code.",
        examples=["+91"],
    )

    currency_code: str | None = Field(
        None,
        min_length=3,
        max_length=3,
        description="ISO 4217 currency code.",
        examples=["INR"],
    )

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str | None) -> str | None:
        """
        Normalize the country name by trimming whitespace and
        converting it to title case.
        """
        return " ".join(value.strip().title().split()) if value else value

    @field_validator("iso2", "iso3", "currency_code")
    @classmethod
    def normalize_codes(cls, value: str | None) -> str | None:
        """
        Normalize ISO and currency codes to uppercase.
        """
        return value.strip().upper() if value else value

    @field_validator("phone_code")
    @classmethod
    def normalize_phone_code(cls, value: str | None) -> str | None:
        """
        Remove leading and trailing whitespace from the phone code.
        """
        return value.strip() if value else value
