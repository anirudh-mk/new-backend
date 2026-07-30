from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    pass  # decoupled: from app.models.company.company import Company
    pass  # decoupled: from app.models.core.currency import Currency
    from app.models.party.party import Party


class PartyCreditLimit(AuditModel):
    """
    Represents the credit policy assigned to a Party.

    Purpose:
        Stores the credit limit configuration for a Party. The credit
        policy determines the maximum outstanding balance that a Party
        is permitted before additional transactions require approval
        or are blocked.

        Credit limits may differ based on company, currency, or business
        requirements and can be modified independently without changing
        the Party master.

    Examples:

        ABC Traders
            Credit Limit : ₹500,000
            Currency     : INR

        XYZ Imports
            Credit Limit : USD 25,000

    ERP Workflow:

        Party
            │
            ▼
        PartyCreditLimit

    Business Benefits:
        - Supports configurable credit limits.
        - Enables multi-currency credit policies.
        - Prevents exceeding customer credit exposure.
        - Reusable across Sales, Finance and Collections.
        - Provides audit history of credit policy changes.

    Relationships:
        Party
            └── PartyCreditLimit

        Company
            └── PartyCreditLimit

        Currency
            └── PartyCreditLimit
    """

    __tablename__ = "party_credit_limits"

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "party_id",
            "currency_id",
            name="uq_party_credit_limit",
        ),
    )

    company_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Company to which this credit policy belongs.",
    )

    party_id: Mapped[UUID] = mapped_column(
        ForeignKey("parties.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Party associated with this credit policy.",
    )

    currency_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Currency in which the credit limit is defined.",
    )

    credit_limit: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Maximum outstanding credit amount allowed for the Party.",
    )

    warning_limit: Mapped[Decimal | None] = mapped_column(
        Numeric(18, 2),
        nullable=True,
        doc="Optional threshold at which warning notifications are generated.",
    )

    grace_days: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
        doc="Additional grace period allowed after the due date.",
    )

    approval_required: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether approval is required when the credit limit is exceeded.",
    )

    remarks: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        doc="Additional notes regarding the credit policy.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
        doc="Indicates whether this credit policy is active.",
    )

    # Relationships


    party: Mapped["Party"] = relationship(
        back_populates="credit_limits",
        lazy="selectin",
        doc="Party associated with this credit policy.",
    )
