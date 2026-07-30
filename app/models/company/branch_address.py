from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.company.branch import Branch
    pass  # decoupled: from app.models.core.address_type import AddressType
    pass  # decoupled: from app.models.core.country import Country
    pass  # decoupled: from app.models.core.state import State
    pass  # decoupled: from app.models.core.district import District


class BranchAddress(AuditModel):
    """
    Represents a physical address associated with a Branch.

    Stores detailed location data (street address, coordinates) and resolves them to
    AddressType, Country, State, and District lookups.

    Purpose:
        - Stores shipping, billing, or warehouse addresses per branch.
        - Supports coordinates for route planning and geographic localization.
    """

    __tablename__ = "branch_addresses"

    branch_id: Mapped[UUID] = mapped_column(
        ForeignKey("branches.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="The branch associated with this address.",
    )

    address_type_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="The classification type of the address (e.g. Billing, Shipping).",
    )

    address_line_1: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        doc="First line of the address.",
    )

    address_line_2: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        doc="Second line of the address.",
    )

    country_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Country of the address.",
    )

    state_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="State or region of the address.",
    )

    district_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="District or county of the address.",
    )

    postal_code: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        doc="ZIP or postal code.",
    )

    latitude: Mapped[float | None] = mapped_column(
        Numeric(10, 8),
        nullable=True,
        doc="Optional GPS latitude coordinate.",
    )

    longitude: Mapped[float | None] = mapped_column(
        Numeric(11, 8),
        nullable=True,
        doc="Optional GPS longitude coordinate.",
    )

    is_primary: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
        doc="Indicates whether this is the primary address for the branch.",
    )

    display_order: Mapped[int] = mapped_column(
        default=1,
        nullable=False,
        doc="Display order sequence number.",
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
        doc="Indicates whether the address record is active.",
    )

    # Relationships
    branch: Mapped["Branch"] = relationship(
        back_populates="addresses",
    )


    def __repr__(self) -> str:
        return f"<BranchAddress(id={self.id}, line_1='{self.address_line_1}', branch_id={self.branch_id})>"