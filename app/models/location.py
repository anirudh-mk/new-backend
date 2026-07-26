from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel


class Country(AuditModel):
    """
    Represents a country.

    Stores country-specific information including ISO codes,
    phone code, currency code, and its associated states.
    """

    __tablename__ = "countries"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    iso2: Mapped[str] = mapped_column(
        String(2),
        unique=True,
        nullable=False,
    )

    iso3: Mapped[str] = mapped_column(
        String(3),
        unique=True,
        nullable=False,
    )

    phone_code: Mapped[str] = mapped_column(
        String(5),
        nullable=False,
    )

    currency_code: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )

    states: Mapped[list["State"]] = relationship(
        back_populates="country",
        cascade="all, delete-orphan",
    )


class State(AuditModel):
    """
    Represents a state or province within a country.

    Each state belongs to a single country and can contain multiple
    districts. State names are unique within the same country and
    optionally include a short code or abbreviation.
    """

    __tablename__ = "states"

    __table_args__ = (
        UniqueConstraint(
            "country_id",
            "name",
            name="uq_state_country_name",
        ),
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    code: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )

    country: Mapped["Country"] = relationship(
        back_populates="states",
    )

    districts: Mapped[list["District"]] = relationship(
        back_populates="state",
        cascade="all, delete-orphan",
    )


class District(AuditModel):
    """
    Represents a district within a state.

    Each district belongs to a single state and can be used to organize
    lower-level administrative entities such as cities or branches.
    """

    __tablename__ = "districts"

    __table_args__ = (
        UniqueConstraint(
            "state_id",
            "name",
            name="uq_district_state_name",
        ),
    )

    state_id: Mapped[UUID] = mapped_column(
        ForeignKey("states.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )

    state: Mapped["State"] = relationship(
        back_populates="districts",
    )
