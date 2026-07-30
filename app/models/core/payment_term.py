from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    pass  # decoupled: from app.models.party.party_payment_term import PartyPaymentTerm


class PaymentTerm(AuditModel):
    """
    Represents a configurable payment term used throughout the ERP.

    Purpose:
        Payment Terms define the agreed payment conditions between the
        company and its business partners. They specify when payment is
        expected after a sale or purchase.

        Payment Terms are maintained as master data and can be assigned
        to Parties, Sales Orders, Purchase Orders, Invoices and other
        financial documents.

    Examples:
        - Cash on Delivery
        - Advance Payment
        - Net 7
        - Net 15
        - Net 30
        - Net 45
        - Net 60
        - End of Month

    ERP Workflow:

        Payment Term
              │
              ▼
        PartyPaymentTerm
              │
              ▼
            Party

              │
              ▼
        Sales Order
        Purchase Order
        Sales Invoice
        Purchase Invoice

    Business Benefits:
        - Centralizes payment policies.
        - Eliminates duplicate payment conditions.
        - Standardizes credit periods.
        - Simplifies receivable and payable management.
        - Reusable across multiple ERP modules.

    Relationships:
        PaymentTerm
            └── PartyPaymentTerm
    """

    __tablename__ = "payment_terms"

    __table_args__ = (
        UniqueConstraint(
            "code",
            name="uq_payment_term_code",
        ),
        UniqueConstraint(
            "name",
            name="uq_payment_term_name",
        ),
    )

    code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
        doc=(
            "Unique business code identifying the payment term. "
            "Examples: NET30, COD, ADVANCE."
        ),
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        doc="Display name of the payment term.",
    )

    days: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        doc=(
            "Number of credit days before payment is due. "
            "A value of 0 indicates immediate payment."
        ),
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        doc="Optional description explaining the payment term.",
    )

    is_system: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc=(
            "Indicates whether this is a system-defined payment term. "
            "System payment terms are typically protected from deletion."
        ),
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
        doc="Indicates whether this payment term is active.",
    )

    # Relationships
