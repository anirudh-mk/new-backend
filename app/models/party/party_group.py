from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.company import Company
    from app.models.party.party import Party


class PartyGroup(AuditModel):
    """
    Represents a logical classification of Parties within a Company.

    Purpose:
        Party Groups organize business partners into meaningful categories
        for reporting, searching, pricing, marketing, credit management,
        and operational purposes.

        Unlike Party Types, which define the business role of a Party
        (Customer, Supplier, Transporter, etc.), Party Groups provide
        business classifications.

    Examples:
        - Retail Customers
        - Wholesale Customers
        - VIP Customers
        - Government Organizations
        - Export Customers
        - Local Suppliers
        - Overseas Suppliers
        - Dealers
        - Distributors

    Difference Between Party Group and Party Type:

        Party Type:
            Defines WHAT a party is.

            Examples:
                Customer
                Supplier
                Transporter

        Party Group:
            Defines HOW parties are categorized.

            Examples:
                Retail
                Wholesale
                Government
                VIP

    ERP Workflow:

        Company
            │
            ▼
        Party Group
            │
            ▼
        Party
            ├── Contacts
            ├── Addresses
            ├── Bank Accounts
            ├── Attachments
            └── Ledger

    Business Benefits:
        - Organizes Parties into meaningful categories.
        - Simplifies searching and filtering.
        - Enables pricing and discount strategies.
        - Supports reporting and analytics.
        - Assists marketing and customer segmentation.
        - Improves operational management.

    Relationships:
        Company
            └── PartyGroup

        PartyGroup
            └── Party
    """

    __tablename__ = "party_groups"

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "code",
            name="uq_party_group_company_code",
        ),
        UniqueConstraint(
            "company_id",
            "name",
            name="uq_party_group_company_name",
        ),
    )

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Company that owns this Party Group.",
    )

    code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
        doc=(
            "Unique business code identifying the Party Group "
            "within the Company."
        ),
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        doc="Display name of the Party Group.",
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        doc="Optional description explaining the purpose of the Party Group.",
    )

    is_system: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc=(
            "Indicates whether this is a system-defined Party Group. "
            "System groups are seeded by the application and are typically "
            "protected from deletion."
        ),
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
        doc="Indicates whether this Party Group is active.",
    )

    # Relationships

    company: Mapped["Company"] = relationship(
        back_populates="party_groups",
        lazy="selectin",
        doc="Company that owns this Party Group.",
    )

    parties: Mapped[list["Party"]] = relationship(
        back_populates="party_group",
        lazy="selectin",
        doc="Collection of Parties assigned to this Party Group.",
    )
