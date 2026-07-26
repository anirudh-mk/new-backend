from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.party.party_type_mapping import PartyTypeMapping


class PartyType(AuditModel):
    """
    Represents a configurable business role that can be assigned to one or more
    Parties within the ERP.

    Purpose:
        Party Types define the business relationship between the company and a
        Party. They describe *what role* a Party plays in business processes
        such as Sales, Purchase, Logistics, Manufacturing, CRM, and Services.

        Unlike hardcoded boolean flags (for example, `is_customer` or
        `is_supplier`), Party Types are fully configurable master data.
        Administrators can introduce new business roles without requiring
        database schema changes or application code modifications.

        A Party may have one or more Party Types through the
        PartyTypeMapping model.

    Examples:
        - Customer
        - Supplier
        - Transporter
        - Distributor
        - Dealer
        - Manufacturer
        - Service Provider
        - Contractor
        - Franchise
        - Agent
        - Broker

    ERP Workflow:

        Party Type
            │
            ▼
        PartyTypeMapping
            │
            ▼
        Party
            │
            ├── Contacts
            ├── Addresses
            ├── Bank Accounts
            ├── Attachments
            └── Ledger

    Business Benefits:
        - Eliminates hardcoded customer/supplier flags.
        - Allows a Party to perform multiple business roles.
        - Supports future business types without database redesign.
        - Centralizes role management.
        - Simplifies reporting and filtering.
        - Improves extensibility for enterprise ERP implementations.

    Typical Usage:

        Customer
            Used by Sales, Receivables and CRM.

        Supplier
            Used by Purchasing and Payables.

        Transporter
            Used for delivery and logistics.

        Manufacturer
            Used for production outsourcing.

        Service Provider
            Used for maintenance and professional services.

        Dealer / Distributor
            Used for channel sales management.

    System Types:
        Certain Party Types may be marked as system-defined
        (`is_system=True`). These records are seeded during installation and
        should not be deleted by end users, although they may be referenced
        throughout the ERP.

    Relationships:
        PartyType
            └── PartyTypeMapping

        PartyTypeMapping
            └── Party

    Example:

        Party Types:
            Customer
            Supplier
            Transporter

        Party:
            ABC Traders

        Mapping:
            ABC Traders
                ├── Customer
                └── Supplier
    """

    __tablename__ = "party_types"
    __table_args__ = (
        UniqueConstraint("code", name="uq_party_type_code"),
        UniqueConstraint("name", name="uq_party_type_name"),
    )
    code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
        doc=(
            "Unique business code identifying the party type. "
            "Examples: CUSTOMER, SUPPLIER, TRANSPORTER."
        ),
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        doc=(
            "Display name of the party type shown throughout the ERP. "
            "Examples: Customer, Supplier, Transporter."
        ),
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        doc=(
            "Optional description explaining the purpose or usage of the "
            "party type."
        ),
    )

    is_system: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc=(
            "Indicates whether this is a system-defined party type. "
            "System types are seeded by the application and are typically "
            "protected from deletion."
        ),
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
        doc=(
            "Indicates whether the party type is available for assignment "
            "to new or existing parties."
        ),
    )
    party_mappings: Mapped[list["PartyTypeMapping"]] = relationship(
        back_populates="party_type",
        cascade="all, delete-orphan",
    )
