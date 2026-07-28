from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.core.state import State


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
