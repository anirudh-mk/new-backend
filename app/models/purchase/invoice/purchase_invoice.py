from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.company.company import Company
    from app.models.company.branch import Branch
    from app.models.party.party import Party
    from app.models.purchase.purchase_order import PurchaseOrder
    from app.models.purchase.purchase_receipt import PurchaseReceipt
    from app.models.purchase.purchase_invoice_item import PurchaseInvoiceItem
    from app.models.accounting.payment_term import PaymentTerm
    from app.models.accounting.journal_status import JournalStatus
    from app.models.core.currency import Currency
    from app.models.purchase.purchase_invoice_type import PurchaseInvoiceType


class PurchaseInvoice(AuditModel):
    """
    Represents a Purchase Invoice received from a supplier.

    Purpose:
        A Purchase Invoice records the supplier's bill for goods or
        services purchased by the company. It is created after receiving
        goods and forms the basis for Accounts Payable and General Ledger
        postings.

    Workflow:

        Purchase Order
              │
              ▼
        Purchase Receipt
              │
              ▼
        Purchase Invoice
              │
              ▼
        Supplier Payment
              │
              ▼
        Journal Entry

    Business Benefits:
        - Records supplier bills.
        - Creates Accounts Payable.
        - Supports multi-currency purchasing.
        - Calculates taxes and discounts.
        - Tracks outstanding balances.
        - Integrates with General Ledger.
        - Supports payment schedules.
        - Provides complete financial audit trails.

    Relationships:
        PurchaseOrder
            └── PurchaseInvoice

        PurchaseReceipt
            └── PurchaseInvoice

        PurchaseInvoice
            ├── PurchaseInvoiceItem
            ├── PurchaseInvoiceTax
            ├── PurchaseInvoiceCharge
            └── PurchaseInvoicePayment
    """

    __tablename__ = "purchase_invoices"

    invoice_no: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
        doc="Internal Purchase Invoice number.",
    )

    invoice_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Purchase Invoice date.",
    )

    supplier_invoice_no: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        doc="Supplier invoice reference number.",
    )

    supplier_invoice_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Supplier invoice date.",
    )

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
    )

    branch_id: Mapped[UUID] = mapped_column(
        ForeignKey("branches.id"),
        nullable=False,
        index=True,
    )

    purchase_order_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("purchase_orders.id"),
        nullable=True,
        index=True,
    )

    purchase_receipt_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("purchase_receipts.id"),
        nullable=True,
        index=True,
    )

    supplier_id: Mapped[UUID] = mapped_column(
        ForeignKey("parties.id"),
        nullable=False,
        index=True,
    )

    currency_id: Mapped[UUID] = mapped_column(
        ForeignKey("currencies.id"),
        nullable=False,
        index=True,
    )

    exchange_rate: Mapped[float] = mapped_column(
        Numeric(18, 6),
        nullable=False,
        default=1,
    )

    payment_term_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("payment_terms.id"),
        nullable=True,
    )

    due_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    subtotal: Mapped[float] = mapped_column(
        Numeric(18, 2),
        default=0,
    )

    discount_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        default=0,
    )

    tax_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        default=0,
    )

    other_charges: Mapped[float] = mapped_column(
        Numeric(18, 2),
        default=0,
    )

    round_off_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        default=0,
    )

    grand_total: Mapped[float] = mapped_column(
        Numeric(18, 2),
        default=0,
    )

    paid_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        default=0,
    )

    balance_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        default=0,
    )

    invoice_type_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("purchase_invoice_types.id"),
        nullable=True,
        index=True,
    )

    remarks: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    status_id: Mapped[UUID] = mapped_column(
        ForeignKey("journal_statuses.id"),
        nullable=False,
        index=True,
    )

    is_posted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    is_cancelled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    company: Mapped["Company"] = relationship()

    branch: Mapped["Branch"] = relationship()

    supplier: Mapped["Party"] = relationship()

    purchase_order: Mapped["PurchaseOrder"] = relationship(
        back_populates="invoices",
    )

    purchase_receipt: Mapped["PurchaseReceipt"] = relationship(
        back_populates="purchase_invoices",
    )

    currency: Mapped["Currency"] = relationship()

    payment_term: Mapped["PaymentTerm"] = relationship()

    invoice_type: Mapped["PurchaseInvoiceType"] = relationship()

    status: Mapped["JournalStatus"] = relationship()

    items: Mapped[list["PurchaseInvoiceItem"]] = relationship(
        back_populates="purchase_invoice",
        cascade="all, delete-orphan",
    )

    taxes: Mapped[list["PurchaseInvoiceTax"]] = relationship(
        back_populates="purchase_invoice",
        cascade="all, delete-orphan",
    )

    charges: Mapped[list["PurchaseInvoiceCharge"]] = relationship(
        back_populates="purchase_invoice",
        cascade="all, delete-orphan",
    )

    payment_schedules: Mapped[list["PurchasePaymentSchedule"]] = relationship(
        back_populates="purchase_invoice",
        cascade="all, delete-orphan",
    )

    payments: Mapped[list["PurchasePaymentAllocation"]] = relationship(
        back_populates="purchase_invoice",
        cascade="all, delete-orphan",
    )

    attachments: Mapped[list["DocumentAttachment"]] = relationship(
        "DocumentAttachment",
        primaryjoin="and_(DocumentAttachment.document_id == PurchaseInvoice.id, "
                    "DocumentAttachment.document_type_id == select(DocumentType.id).where(DocumentType.code == 'PINV').scalar_subquery())",
        foreign_keys="[DocumentAttachment.document_id]",
        cascade="all, delete-orphan",
    )

    approvals: Mapped[list["Approval"]] = relationship(
        "Approval",
        primaryjoin="and_(Approval.document_id == PurchaseInvoice.id, "
                    "Approval.document_type_id == select(DocumentType.id).where(DocumentType.code == 'PINV').scalar_subquery())",
        foreign_keys="[Approval.document_id]",
        cascade="all, delete-orphan",
    )

    status_history: Mapped[list["StatusHistory"]] = relationship(
        "StatusHistory",
        primaryjoin="and_(StatusHistory.document_id == PurchaseInvoice.id, "
                    "StatusHistory.document_type_id == select(DocumentType.id).where(DocumentType.code == 'PINV').scalar_subquery())",
        foreign_keys="[StatusHistory.document_id]",
        cascade="all, delete-orphan",
    )

    audit_history: Mapped[list["AuditHistory"]] = relationship(
        "AuditHistory",
        primaryjoin="and_(AuditHistory.document_id == PurchaseInvoice.id, "
                    "AuditHistory.document_type_id == select(DocumentType.id).where(DocumentType.code == 'PINV').scalar_subquery())",
        foreign_keys="[AuditHistory.document_id]",
        cascade="all, delete-orphan",
    )