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
    from app.models.sales.master.sales_person import SalesPerson
    from app.models.workflow.approval_workflow import ApprovalWorkflow
    from app.models.sales.return_.sales_return_item import SalesReturnItem


class SalesReturn(BaseModel):
    """
    Represents a Customer Sales Return document.

    Purpose:
        A Sales Return records goods returned by a customer
        after a Sales Invoice has been issued.

        It is used to receive returned inventory,
        adjust Accounts Receivable,
        create Credit Notes,
        update stock,
        calculate refund amounts,
        and maintain complete traceability.

        A Sales Return may be created for:

        • Damaged products
        • Defective products
        • Wrong shipment
        • Customer rejection
        • Excess quantity delivered
        • Warranty replacement
        • Product recall

    Examples:

        Invoice

            INV-2026-000145

        Return

            SR-2026-000018

        Customer

            ABC Super Market

        Returned Items

            5 Laptop
            2 Printer

    Workflow:

            Sales Invoice
                   │
                   ▼
             Sales Return
                   │
         ┌─────────┼──────────┐
         ▼         ▼          ▼
    Stock Receipt Credit Note Refund
                   │
                   ▼
           Accounting Entry

    Benefits:

        • Customer return processing.
        • Inventory adjustment.
        • Credit Note generation.
        • Refund management.
        • Warranty handling.
        • Replacement processing.
        • Financial adjustment.
        • Audit trail.
        • Complete traceability.
        • Customer satisfaction.

    Relationships:

               Company
                  │
                  ▼
            SalesReturn
      ┌────────┼────────┬─────────┐
      ▼        ▼        ▼         ▼
 Customer  Invoice  SalesPerson  Items

    Example:

        Return Number

            SR-2026-000018

        Customer

            ABC Super Market

        Return Reason

            Damaged During Transport

        Total

            ₹42,500

    Notes:

        • One Sales Return contains multiple items.
        • One Invoice may have multiple returns.
        • Supports partial returns.
        • Inventory is increased after approval.
        • Credit Notes may be generated.
        • Refunds may be processed.
        • Historical records should never change.
        • Supports approval workflow.

    This model is referenced throughout
    Sales,
    Inventory,
    Warehouse,
    Finance,
    Accounts Receivable,
    Customer Service,
    Warranty,
    Reporting,
    Analytics,
    and Compliance modules.
    """

    __tablename__ = "sales_returns"

    return_number: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
        doc="Unique Sales Return number.",
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

    sales_invoice_id: Mapped[UUID] = mapped_column(
        ForeignKey("sales_invoices.id"),
        nullable=False,
        index=True,
        doc="Reference to the originating Sales Invoice.",
    )

    customer_id: Mapped[UUID] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
        index=True,
        doc="Reference to the Customer.",
    )

    sales_person_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("sales_persons.id"),
        nullable=True,
        index=True,
        doc="Sales Person handling the return.",
    )

    approval_workflow_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("approval_workflows.id"),
        nullable=True,
        index=True,
        doc="Approval workflow assigned to this return.",
    )

    return_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Date of the Sales Return.",
    )

    return_reason: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        doc="Primary reason for the return.",
    )

    refund_method: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
        doc="Refund method such as Cash, Credit Note, Replacement or Bank Transfer.",
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
        doc="Total tax amount.",
    )

    other_charges: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Additional deductions or charges.",
    )

    grand_total: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Total return amount.",
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="DRAFT",
        doc="Current Sales Return status.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Internal remarks.",
    )

    customer_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Customer-facing notes.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether this Sales Return is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    company: Mapped["Company"] = relationship(
        back_populates="sales_returns",
    )

    branch: Mapped["Branch"] = relationship(
        back_populates="sales_returns",
    )

    sales_invoice: Mapped["SalesInvoice"] = relationship(
        back_populates="sales_returns",
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="sales_returns",
    )

    sales_person: Mapped["SalesPerson"] = relationship(
        back_populates="sales_returns",
    )

    approval_workflow: Mapped["ApprovalWorkflow"] = relationship()

    items: Mapped[list["SalesReturnItem"]] = relationship(
        back_populates="sales_return",
        cascade="all, delete-orphan",
    )