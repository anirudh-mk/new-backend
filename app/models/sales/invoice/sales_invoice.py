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
    from app.models.sales.order.sales_order import SalesOrder
    from app.models.sales.delivery.delivery_note import DeliveryNote
    from app.models.sales.master.sales_person import SalesPerson
    from app.models.sales.master.sales_price_list import SalesPriceList
    from app.models.sales.master.sales_terms import SalesTerms
    from app.models.workflow.approval_workflow import ApprovalWorkflow
    from app.models.sales.invoice.sales_invoice_item import SalesInvoiceItem


class SalesInvoice(BaseModel):
    """
    Represents a Customer Sales Invoice.

    Purpose:
        A Sales Invoice is the official financial document
        issued to a customer requesting payment for
        goods delivered or services rendered.

        It is the final commercial document in the
        Sales process and forms the basis for
        Accounts Receivable, Tax Reporting,
        Revenue Recognition, and Customer Payments.

        A Sales Invoice may be generated from:

            • Sales Order
            • Delivery Note
            • Direct Sale

        One Sales Order may generate multiple invoices,
        allowing partial invoicing.

    Examples:

        Sales Order

            SO-2026-000125

        Delivery Note

            DN-2026-000087

        Invoice

            INV-2026-000145

        Customer

            ABC Super Market

        Total

            ₹4,85,250

    Workflow:

          Sales Quotation
                  │
                  ▼
             Sales Order
                  │
                  ▼
            Delivery Note
                  │
                  ▼
            Sales Invoice
                  │
                  ▼
        Accounts Receivable
                  │
                  ▼
          Customer Payment

    Benefits:

        • Customer billing.
        • Revenue recognition.
        • Tax calculation.
        • Accounts receivable integration.
        • Partial invoicing.
        • Multi-currency support.
        • Complete audit trail.
        • Payment tracking.
        • Financial reporting.
        • Regulatory compliance.

    Relationships:

                 Company
                    │
                    ▼
              SalesInvoice
      ┌────────┼────────┼──────────┬─────────┐
      ▼        ▼        ▼          ▼         ▼
 Customer  SalesOrder Delivery  SalesPerson Items
                        Note

    Example:

        Invoice Number

            INV-2026-000145

        Customer

            ABC Super Market

        Invoice Date

            25-Aug-2026

        Grand Total

            ₹4,85,250

        Status

            Posted

    Notes:

        • One invoice contains multiple items.
        • Supports partial invoicing.
        • Supports tax invoices.
        • Supports credit notes.
        • Historical invoices should never be edited.
        • Accounting entries are generated after posting.
        • Supports GST/VAT compliance.
        • Used for customer statements.

    This model is referenced throughout
    Sales,
    Accounts Receivable,
    Finance,
    Taxation,
    Inventory,
    CRM,
    Reporting,
    Analytics,
    Customer Portal,
    and Compliance modules.
    """

    __tablename__ = "sales_invoices"

    invoice_number: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
        doc="Unique Sales Invoice number.",
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

    sales_order_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("sales_orders.id"),
        nullable=True,
        index=True,
        doc="Reference to the originating Sales Order.",
    )

    delivery_note_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("delivery_notes.id"),
        nullable=True,
        index=True,
        doc="Reference to the Delivery Note.",
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
        doc="Assigned Sales Person.",
    )

    sales_price_list_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("sales_price_lists.id"),
        nullable=True,
        index=True,
        doc="Applied Sales Price List.",
    )

    sales_terms_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("sales_terms.id"),
        nullable=True,
        index=True,
        doc="Applied Sales Terms.",
    )

    approval_workflow_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("approval_workflows.id"),
        nullable=True,
        index=True,
        doc="Approval Workflow used for the invoice.",
    )

    invoice_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Invoice date.",
    )

    due_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        doc="Customer payment due date.",
    )

    currency_code: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="INR",
        doc="Invoice currency.",
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Subtotal before discounts and taxes.",
    )

    discount_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Document discount amount.",
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
        doc="Freight, insurance and additional charges.",
    )

    grand_total: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Final invoice amount.",
    )

    paid_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Amount already received.",
    )

    balance_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Outstanding customer balance.",
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="DRAFT",
        doc="Current invoice status.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Internal remarks.",
    )

    customer_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Customer-facing notes printed on the invoice.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether the invoice is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    company: Mapped["Company"] = relationship(
        back_populates="sales_invoices",
    )

    branch: Mapped["Branch"] = relationship(
        back_populates="sales_invoices",
    )

    sales_order: Mapped["SalesOrder"] = relationship(
        back_populates="sales_invoices",
    )

    delivery_note: Mapped["DeliveryNote"] = relationship(
        back_populates="sales_invoices",
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="sales_invoices",
    )

    sales_person: Mapped["SalesPerson"] = relationship(
        back_populates="sales_invoices",
    )

    sales_price_list: Mapped["SalesPriceList"] = relationship()

    sales_terms: Mapped["SalesTerms"] = relationship()

    approval_workflow: Mapped["ApprovalWorkflow"] = relationship()

    items: Mapped[list["SalesInvoiceItem"]] = relationship(
        back_populates="sales_invoice",
        cascade="all, delete-orphan",
    )