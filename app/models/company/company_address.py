from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.company.company import Company
    from app.models.core.address_type import AddressType
    from app.models.core.country import Country
    from app.models.core.state import State
    from app.models.core.district import District


class CompanyAddress(AuditModel):
    """
    Represents a physical or mailing address associated with a Company.

    A CompanyAddress stores location details (street, postal code, coordinates)
    and maps them to a specific AddressType (e.g., Billing, Shipping, Head Office)
    and geographical lookup tables (Country, State, District).

    Purpose:
        - Stores addresses for tax registration, invoicing, and logistics.
        - Identifies primary/default locations for standard transactions.
        - Supports coordinates (latitude/longitude) for shipping and delivery mapping.
    """

    __tablename__ = "company_addresses"

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="The company associated with this address.",
    )

    address_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("address_types.id"),
        nullable=False,
        index=True,
        doc="The classification type of the address (Billing, Shipping, etc.).",
    )

    address_line_1: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        doc="First line of the address (Street number, building name).",
    )

    address_line_2: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        doc="Second line of the address (Suite, apartment, unit number).",
    )

    country_id: Mapped[UUID] = mapped_column(
        ForeignKey("countries.id"),
        nullable=False,
        index=True,
        doc="Country of the address.",
    )

    state_id: Mapped[UUID] = mapped_column(
        ForeignKey("states.id"),
        nullable=False,
        index=True,
        doc="State or region of the address.",
    )

    district_id: Mapped[UUID] = mapped_column(
        ForeignKey("districts.id"),
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
        doc="Indicates whether this is the primary address for the company.",
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
    company: Mapped["Company"] = relationship(
        back_populates="addresses",
    )

    address_type: Mapped["AddressType"] = relationship()
    country: Mapped["Country"] = relationship()
    state: Mapped["State"] = relationship()
    district: Mapped["District"] = relationship()

    def __repr__(self) -> str:
        return f"<CompanyAddress(id={self.id}, line_1='{self.address_line_1}', type_id={self.address_type_id})>"
