from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.party.party import Party
    pass  # decoupled: from app.models.accounting.payment_term import PaymentTerm


class PartyPaymentTerm(AuditModel):
    """
    Associates a Payment Term with a Party.

    Purpose:
        Stores one or more payment terms assigned to a Party. Payment
        Terms define the agreed credit period and payment conditions
        used during sales, purchasing, invoicing and financial
        transactions.

        A Party may have multiple Payment Terms, with one designated
        as the default for business transactions.

    Examples:

        ABC Traders

            • Net 30 (Default)
            • Advance Payment

        XYZ Suppliers

            • Net 60

    ERP Workflow:

        PaymentTerm
              │
              ▼
        PartyPaymentTerm
              │
              ▼
            Party

    Business Benefits:
        - Supports multiple payment terms per Party.
        - Allows a default payment term.
        - Centralizes payment policy management.
        - Reusable across Sales, Purchase and Accounting modules.

    Relationships:
        Party
            └── PartyPaymentTerm

        PaymentTerm
            └── PartyPaymentTerm
    """

    __tablename__ = "party_payment_terms"

    __table_args__ = (
        UniqueConstraint(
            "party_id",
            "payment_term_id",
            name="uq_party_payment_term",
        ),
    )

    party_id: Mapped[UUID] = mapped_column(
        ForeignKey("parties.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Party associated with this payment term.",
    )

    payment_term_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Payment Term assigned to the Party.",
    )

    is_default: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        index=True,
        doc="Indicates whether this is the default payment term for the Party.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
        doc="Indicates whether this payment term assignment is active.",
    )

    # Relationships

    party: Mapped["Party"] = relationship(
        back_populates="payment_terms",
        lazy="selectin",
        doc="Party associated with this payment term assignment.",
    )
