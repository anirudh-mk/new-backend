from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.core.country import Country
    from app.models.core.district import District


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

    country_id: Mapped[UUID] = mapped_column(
        ForeignKey("countries.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
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