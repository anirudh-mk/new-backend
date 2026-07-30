from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    pass  # decoupled: from app.models.core.country import Country
    pass  # decoupled: from app.models.core.address_type import AddressType
    from app.models.party.party import Party
    pass  # decoupled: from app.models.core.state import State


class PartyAddress(AuditModel):
    """
    Represents a physical or mailing address associated with a Party.

    Purpose:
        Stores one or more addresses for a Party. A Party may maintain
        different addresses for billing, shipping, registered office,
        warehouse, branch office, or other operational purposes.

        Address types are maintained separately through the AddressType
        master, allowing organizations to introduce new address
        classifications without changing the database schema.

    Examples:

        ABC Traders

            • Billing Address
            • Shipping Address
            • Registered Office
            • Warehouse

    ERP Workflow:

        Party
            │
            ▼
        PartyAddress
            │
            ├── Billing
            ├── Shipping
            ├── Office
            └── Warehouse

    Business Benefits:
        - Supports multiple addresses per Party.
        - Eliminates duplicate address records.
        - Enables configurable address classifications.
        - Simplifies invoicing, shipping and reporting.
        - Supports future logistics and CRM modules.

    Relationships:
        Party
            └── PartyAddress

        AddressType
            └── PartyAddress

        Country
            └── PartyAddress

        State
            └── PartyAddress
    """

    __tablename__ = "party_addresses"

    __table_args__ = (
        UniqueConstraint(
            "party_id",
            "address_type_id",
            "address_line_1",
            "postal_code",
            name="uq_party_address",
        ),
    )

    party_id: Mapped[UUID] = mapped_column(
        ForeignKey("parties.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Party that owns this address.",
    )

    address_type_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Classification of the address (Billing, Shipping, Office, Warehouse, etc.).",
    )

    address_line_1: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        doc="Primary address line.",
    )

    address_line_2: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        doc="Secondary address line.",
    )

    landmark: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
        doc="Nearby landmark for easier identification.",
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        doc="City or town.",
    )

    state_id: Mapped[UUID | None] = mapped_column(
        nullable=True,
        index=True,
        doc="State or province.",
    )

    country_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Country.",
    )

    postal_code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
        doc="ZIP or postal code.",
    )

    latitude: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
        doc="Latitude coordinate.",
    )

    longitude: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
        doc="Longitude coordinate.",
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional delivery or address instructions.",
    )

    is_default: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        index=True,
        doc="Indicates whether this is the default address of its type.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
        doc="Indicates whether this address is active.",
    )

    # Relationships

    party: Mapped["Party"] = relationship(
        back_populates="addresses",
        lazy="selectin",
        doc="Party associated with this address.",
    )


