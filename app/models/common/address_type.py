from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.party.party_address import PartyAddress


class AddressType(AuditModel):
    """
    Represents a configurable classification for Party Addresses.

    Purpose:
        Address Types define the business purpose of an address associated
        with a Party. Rather than hardcoding values such as Billing or
        Shipping, address classifications are maintained as configurable
        master data.

        A Party may have multiple addresses, each assigned a different
        Address Type.

    Examples:
        - Billing
        - Shipping
        - Registered Office
        - Head Office
        - Branch Office
        - Warehouse
        - Factory
        - Home

    ERP Workflow:

        Address Type
              │
              ▼
        Party Address
              │
              ▼
            Party

    Business Benefits:
        - Eliminates hardcoded address types.
        - Supports unlimited address classifications.
        - Simplifies reporting and filtering.
        - Enables future address types without schema changes.
        - Reusable across ERP modules.

    Relationships:
        AddressType
            └── PartyAddress
    """

    __tablename__ = "address_types"

    __table_args__ = (
        UniqueConstraint(
            "code",
            name="uq_address_type_code",
        ),
        UniqueConstraint(
            "name",
            name="uq_address_type_name",
        ),
    )

    code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
        doc=(
            "Unique business code identifying the address type. "
            "Examples: BILLING, SHIPPING, OFFICE."
        ),
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        doc="Display name of the address type.",
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        doc="Optional description explaining the purpose of the address type.",
    )

    is_system: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc=(
            "Indicates whether this is a system-defined address type. "
            "System types are typically protected from deletion."
        ),
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
        doc="Indicates whether this address type is active.",
    )

    # Relationships

    addresses: Mapped[list["PartyAddress"]] = relationship(
        back_populates="address_type",
        cascade="all, delete-orphan",
        lazy="selectin",
        doc="Collection of Party Addresses assigned to this address type.",
    )
