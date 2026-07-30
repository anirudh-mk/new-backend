from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.sales.payment.customer_receipt import CustomerReceipt
    from app.models.sales.invoice.sales_invoice import SalesInvoice


class CustomerReceiptItem(BaseModel):
    """
    Represents an individual invoice allocation within a Customer Receipt.

    Purpose:
        Customer Receipt Item stores each invoice or
        financial document settled by a Customer Receipt.

        Each Customer Receipt consists of one or more
        Receipt Items.

        Every line represents the allocation of a payment
        towards a Sales Invoice.

        This model enables:

        • Multiple invoice settlement
        • Partial invoice payment
        • Advance allocation
        • Outstanding balance tracking
        • Accounts Receivable reconciliation

    Examples:

        Receipt

            CR-2026-000125

        Invoice

            INV-2026-000451

        Paid

            ₹25,000

        ------------------------------------

        Invoice

            INV-2026-000452

        Paid

            ₹15,000

    Workflow:

            Customer Receipt
                    │
                    ▼
          Customer Receipt Item
                    │
        ┌───────────┼────────────┐
        ▼           ▼            ▼
    Invoice      AR Update   GL Posting

    Benefits:

        • Supports multiple invoices.
        • Supports partial payments.
        • Tracks outstanding balances.
        • Supports advance allocation.
        • Improves auditability.
        • Simplifies reconciliation.
        • Financial reporting.
        • Customer statement generation.
        • Complete payment history.

    Relationships:

            CustomerReceipt
                    │
                    ▼
          CustomerReceiptItem
                    │
                    ▼
             SalesInvoice

    Example:

        Invoice

            INV-2026-000451

        Invoice Amount

            ₹50,000

        Allocated

            ₹30,000

        Remaining

            ₹20,000

    Notes:

        • One receipt may contain multiple items.
        • One invoice may receive multiple payments.
        • Supports partial settlement.
        • Historical values should never change.
        • Used for AR aging reports.
        • Used during bank reconciliation.

    Referenced by
    Sales,
    Accounts Receivable,
    Finance,
    Banking,
    Customer Statements,
    Reporting,
    Analytics,
    and Compliance modules.
    """

    __tablename__ = "customer_receipt_items"

    customer_receipt_id: Mapped[UUID] = mapped_column(
        ForeignKey("customer_receipts.id"),
        nullable=False,
        index=True,
        doc="Reference to the Customer Receipt.",
    )

    sales_invoice_id: Mapped[UUID] = mapped_column(
        ForeignKey("sales_invoices.id"),
        nullable=False,
        index=True,
        doc="Reference to the Sales Invoice being settled.",
    )

    line_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        doc="Sequential line number within the receipt.",
    )

    invoice_number: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        doc="Invoice number copied for reporting purposes.",
    )

    invoice_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Original invoice amount.",
    )

    outstanding_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Outstanding amount before allocation.",
    )

    allocated_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Amount allocated from this receipt.",
    )

    remaining_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Outstanding balance after allocation.",
    )

    allocation_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="ALLOCATED",
        doc="Allocation status (ALLOCATED, PARTIAL, ADVANCE).",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Remarks for this allocation.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether this receipt item is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------


    sales_invoice: Mapped["SalesInvoice"] = relationship(
        back_populates="receipt_items",
    )