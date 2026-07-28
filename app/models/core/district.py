from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.core.state import State


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
