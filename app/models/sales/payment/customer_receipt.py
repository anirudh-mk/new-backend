from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    Date,
    ForeignKey,
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
    from app.models.company.company import Company
    from app.models.company.branch import Branch
    from app.models.party.customer.customer import Customer
    from app.models.accounting.payment.payment_method import PaymentMethod
    from app.models.sales.payment.customer_receipt_item import (
        CustomerReceiptItem,
    )


class CustomerReceipt(BaseModel):
    """
    Represents a Customer Receipt received against one or more
    Sales Invoices.

    Purpose:
        Customer Receipt records payments received from
        customers through Cash, Bank Transfer,
        Cheque, UPI, Credit Card,
        Debit Card, Online Gateway,
        or any supported payment method.

        A receipt may settle:

        • One Invoice
        • Multiple Invoices
        • Partial Invoice Payments
        • Advance Payments
        • Over Payments
        • Customer Deposits

        This document updates Accounts Receivable,
        creates General Ledger entries,
        reconciles bank transactions,
        and maintains customer outstanding balances.

    Examples:

        Receipt No

            CR-2026-000145

        Customer

            ABC Super Market

        Amount

            ₹2,50,000

        Payment Method

            Bank Transfer

    Workflow:

            Sales Invoice
                   │
                   ▼
          Customer Receipt
          ┌────────┼─────────┐
          ▼        ▼         ▼
     AR Update   Bank GL   Allocation
                   │
                   ▼
           Outstanding Reduced

    Benefits:

        • Supports multiple invoices.
        • Supports partial payments.
        • Supports advance receipts.
        • Supports customer deposits.
        • Automatic AR reconciliation.
        • Bank reconciliation.
        • Financial reporting.
        • Audit trail.
        • Multi-payment support.
        • Multi-currency ready.

    Relationships:

              Company
                 │
                 ▼
          CustomerReceipt
      ┌────────┼────────┬─────────┐
      ▼        ▼        ▼         ▼
   Customer  Payment  Invoice  Allocation

    Example:

        Customer

            ABC Super Market

        Payment

            ₹75,000

        Method

            UPI

        Status

            Completed

    Notes:

        • One receipt may settle multiple invoices.
        • Supports advance receipts.
        • Supports partial invoice settlement.
        • Accounting entries generated automatically.
        • Historical values should never change.
        • Used for AR aging reports.
        • Used during bank reconciliation.

    This model is referenced throughout
    Sales,
    Accounts Receivable,
    Accounting,
    Finance,
    Banking,
    Customer Portal,
    Reporting,
    Analytics,
    Cash Management,
    and Compliance modules.
    """

    __tablename__ = "customer_receipts"

    receipt_number: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
        doc="Unique Customer Receipt number.",
    )

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
        doc="Reference to the Company.",
    )

    branch_id: Mapped[UUID] = mapped_column(
        ForeignKey("branches.id"),
        nullable=False,
        index=True,
        doc="Reference to the Branch.",
    )

    customer_id: Mapped[UUID] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
        index=True,
        doc="Customer making the payment.",
    )

    payment_method_id: Mapped[UUID] = mapped_column(
        ForeignKey("payment_methods.id"),
        nullable=False,
        index=True,
        doc="Payment method used for the receipt.",
    )

    receipt_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Date the payment was received.",
    )

    reference_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        doc="Cheque number, UTR, Transaction ID or Gateway Reference.",
    )

    currency_code: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="INR",
        doc="Receipt currency.",
    )

    exchange_rate: Mapped[Decimal] = mapped_column(
        Numeric(18, 6),
        nullable=False,
        default=1,
        doc="Exchange rate used for foreign currency receipts.",
    )

    received_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Total amount received.",
    )

    allocated_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Amount allocated to invoices.",
    )

    unallocated_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Remaining amount available for future allocation.",
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="POSTED",
        doc="Receipt status.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Internal remarks.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether this receipt is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    company: Mapped["Company"] = relationship(
        back_populates="customer_receipts",
    )

    branch: Mapped["Branch"] = relationship(
        back_populates="customer_receipts",
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="customer_receipts",
    )

    payment_method: Mapped["PaymentMethod"] = relationship(
        back_populates="customer_receipts",
    )

    items: Mapped[list["CustomerReceiptItem"]] = relationship(
        back_populates="customer_receipt",
        cascade="all, delete-orphan",
    )