from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Date,
    ForeignKey,
    Numeric,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.company.company import Company
    from app.models.company.branch import Branch
    from app.models.core.journal_status import JournalStatus
    from app.models.purchase.invoice.purchase_invoice import PurchaseInvoice


class PurchasePaymentSchedule(BaseModel):
    """
    Represents a scheduled payment installment for a Purchase Invoice.

    Purpose:
        Purchase Payment Schedule defines the planned payment installments
        for supplier invoices. Each Purchase Invoice may contain one or
        more scheduled payments based on the agreed payment terms.

        Actual payments are recorded separately in the
        PurchaseInvoicePayment model.

    Workflow:

        Purchase Invoice
                │
                ▼
        Purchase Payment Schedule
                │
                ▼
        Purchase Invoice Payment

    Example:

        Invoice Amount : ₹1,00,000

        Installment 1
            Due Date : 01-Jul-2026
            Amount   : ₹40,000

        Installment 2
            Due Date : 01-Aug-2026
            Amount   : ₹30,000

        Installment 3
            Due Date : 01-Sep-2026
            Amount   : ₹30,000

    Benefits:

        • Supports installment payments
        • Credit purchase management
        • Accounts Payable aging
        • Due payment reminders
        • Outstanding balance tracking
        • Financial reporting

    Relationships:

        PurchaseInvoice
                │
                └── PurchasePaymentSchedule

        JournalStatus
                │
                └── PurchasePaymentSchedule

        Company
                │
                └── PurchasePaymentSchedule

        Branch
                │
                └── PurchasePaymentSchedule
    """

    __tablename__ = "purchase_payment_schedules"

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
        doc="Company that owns this payment schedule.",
    )

    branch_id: Mapped[UUID] = mapped_column(
        ForeignKey("branches.id"),
        nullable=False,
        index=True,
        doc="Branch that owns this payment schedule.",
    )

    purchase_invoice_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_invoices.id"),
        nullable=False,
        index=True,
        doc="Reference to the Purchase Invoice.",
    )

    installment_no: Mapped[int] = mapped_column(
        nullable=False,
        doc="Installment sequence number.",
    )

    due_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Scheduled payment due date.",
    )

    scheduled_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Scheduled payment amount.",
    )

    paid_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Amount paid against this installment.",
    )

    balance_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Outstanding balance for this installment.",
    )

    status_id: Mapped[UUID] = mapped_column(
        ForeignKey("journal_statuses.id"),
        nullable=False,
        index=True,
        doc="Current payment schedule status.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional remarks.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    company: Mapped["Company"] = relationship()

    branch: Mapped["Branch"] = relationship()

    purchase_invoice: Mapped["PurchaseInvoice"] = relationship(
        back_populates="payment_schedules",
    )

    status: Mapped["JournalStatus"] = relationship()