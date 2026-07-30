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
    from app.models.sales.invoice.sales_invoice import SalesInvoice
    from app.models.sales.return_.sales_return import SalesReturn
    from app.models.sales.master.sales_person import SalesPerson
    from app.models.workflow.approval_workflow import ApprovalWorkflow
    from app.models.sales.credit_note.credit_note_item import CreditNoteItem


class CreditNote(BaseModel):
    """
    Represents a Customer Credit Note.

    Purpose:
        Credit Note is a financial document issued to reduce
        the amount owed by a customer after a Sales Invoice
        has been posted.

        Credit Notes are commonly created from Sales Returns,
        pricing adjustments, discounts, damaged goods,
        billing errors, warranty claims, or customer goodwill.

        Instead of refunding cash immediately,
        the amount may remain as customer credit
        for future invoices.

    Examples:

        • Sales Return
        • Invoice Correction
        • Price Difference
        • Damaged Goods
        • Promotional Discount
        • Warranty Settlement
        • Customer Compensation

    Workflow:

            Sales Invoice
                   │
         ┌─────────┴──────────┐
         ▼                    ▼
    Sales Return      Manual Adjustment
         │                    │
         └──────────┬─────────┘
                    ▼
              Credit Note
                    │
         ┌──────────┼───────────┐
         ▼          ▼           ▼
     Customer AR   GL Entry   Future Invoice

    Benefits:

        • Customer balance adjustment.
        • Partial credit support.
        • Full credit support.
        • Linked to Sales Return.
        • Financial audit trail.
        • Credit balance management.
        • Accounting integration.
        • Tax adjustment.
        • Customer statement support.
        • Regulatory compliance.

    Relationships:

              Company
                 │
                 ▼
             CreditNote
      ┌────────┼────────┬────────┬─────────┐
      ▼        ▼        ▼        ▼
 Customer  Invoice  Return  Credit Items

    Example:

        Credit Note No

            CN-2026-000025

        Customer

            ABC Super Market

        Credit Amount

            ₹24,500

        Reason

            Returned Damaged Goods

    Notes:

        • One Credit Note contains multiple items.
        • One Invoice may have multiple Credit Notes.
        • Supports partial credits.
        • Supports future invoice adjustments.
        • Historical values should never change.
        • Accounting entries generated automatically.
        • Approval workflow supported.

    This model is referenced throughout
    Sales,
    Accounts Receivable,
    Finance,
    Accounting,
    Customer Service,
    Reporting,
    Analytics,
    Taxation,
    and Compliance modules.
    """

    __tablename__ = "credit_notes"

    credit_note_number: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
        doc="Unique Credit Note number.",
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
        doc="Customer receiving the credit.",
    )

    sales_invoice_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("sales_invoices.id"),
        nullable=True,
        index=True,
        doc="Related Sales Invoice.",
    )

    sales_return_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("sales_returns.id"),
        nullable=True,
        index=True,
        doc="Related Sales Return.",
    )

    sales_person_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("sales_persons.id"),
        nullable=True,
        index=True,
        doc="Sales Person responsible for the Credit Note.",
    )

    approval_workflow_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("approval_workflows.id"),
        nullable=True,
        index=True,
        doc="Approval workflow assigned to this Credit Note.",
    )

    credit_note_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Credit Note date.",
    )

    reason: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        doc="Reason for issuing the Credit Note.",
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Subtotal before taxes.",
    )

    tax_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Total tax adjustment.",
    )

    other_charges: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Additional charges or deductions.",
    )

    grand_total: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Total Credit Note value.",
    )

    utilized_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Amount already utilized.",
    )

    balance_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Remaining credit balance.",
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="DRAFT",
        doc="Current Credit Note status.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Internal remarks.",
    )

    customer_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Customer-facing remarks.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether this Credit Note is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    company: Mapped["Company"] = relationship(
        back_populates="credit_notes",
    )

    branch: Mapped["Branch"] = relationship(
        back_populates="credit_notes",
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="credit_notes",
    )

    sales_invoice: Mapped["SalesInvoice"] = relationship(
        back_populates="credit_notes",
    )

    sales_return: Mapped["SalesReturn"] = relationship(
        back_populates="credit_notes",
    )

    sales_person: Mapped["SalesPerson"] = relationship(
        back_populates="credit_notes",
    )

    approval_workflow: Mapped["ApprovalWorkflow"] = relationship()

    items: Mapped[list["CreditNoteItem"]] = relationship(
        back_populates="credit_note",
        cascade="all, delete-orphan",
    )