from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.party.party import Party
    from app.models.party.party_type import PartyType


class PartyTypeMapping(AuditModel):
    """
    Maps a Party to one or more Party Types.

    Purpose:
        A Party represents a business entity such as a customer, supplier,
        transporter, distributor, dealer, contractor, or any other external
        entity with whom the company conducts business.

        Since a single business entity may perform multiple roles, this model
        provides a many-to-many relationship between Party and PartyType.

        This design eliminates the need for multiple boolean fields such as
        `is_customer` or `is_supplier` and allows the ERP to support new
        business roles without modifying the database schema.

    Examples:
        ABC Traders
            ├── Customer
            └── Supplier

        XYZ Logistics
            └── Transporter

        Global Technologies
            ├── Customer
            ├── Service Provider
            └── Distributor

    Why this model exists:
        Consider a company that purchases raw materials from a vendor and later
        sells finished goods back to the same company.

        Instead of creating two separate records:

            Customer
                ABC Industries

            Supplier
                ABC Industries

        only one Party is created:

            Party
                ABC Industries

        and multiple business roles are assigned:

            Customer
            Supplier

        This avoids duplicate master data and provides a single source of truth
        for addresses, contacts, bank accounts, tax registrations, documents,
        and accounting ledgers.

    ERP Workflow:

        Company
            │
            ▼
        Party
            │
            ▼
        PartyTypeMapping
            │
            ├── Customer
            ├── Supplier
            ├── Transporter
            ├── Dealer
            └── Service Provider

    Business Benefits:
        - Supports multiple business roles for a single Party.
        - Eliminates duplicate Customer and Supplier records.
        - Centralizes master data.
        - Allows new Party Types without database redesign.
        - Simplifies reporting and maintenance.
        - Provides flexibility for future ERP modules.

    Database Constraints:
        - A Party may have multiple Party Types.
        - A Party Type may be assigned to multiple Parties.
        - Duplicate Party-Type combinations are prevented by a unique constraint.

    Relationships:
        Party
            └── PartyTypeMapping

        PartyType
            └── PartyTypeMapping

    Example:

        Party:
            ABC Traders

        Party Types:
            Customer
            Supplier

        Mapping:
            ABC Traders → Customer
            ABC Traders → Supplier
    """

    __tablename__ = "party_type_mappings"

    __table_args__ = (
        UniqueConstraint(
            "party_id",
            "party_type_id",
            name="uq_party_type_mapping",
        ),
    )

    party_id: Mapped[UUID] = mapped_column(
        ForeignKey("parties.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc=(
            "Reference to the Party that is being assigned a business role. "
            "A single Party may have multiple Party Type mappings."
        ),
    )

    party_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("party_types.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        doc=(
            "Reference to the Party Type assigned to the Party, "
            "such as Customer, Supplier, Transporter or Dealer."
        ),
    )

    # Relationships

    party: Mapped["Party"] = relationship(
        back_populates="party_type_mappings",
        lazy="selectin",
        doc=(
            "The Party associated with this mapping. "
            "Represents the business entity receiving the assigned role."
        ),
    )

    party_type: Mapped["PartyType"] = relationship(
        back_populates="party_mappings",
        lazy="selectin",
        doc=(
            "The business role assigned to the Party. "
            "Examples include Customer, Supplier, Transporter, "
            "Distributor and Service Provider."
        ),
    )
