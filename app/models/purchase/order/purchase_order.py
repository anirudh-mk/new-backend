from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    pass  # decoupled: from app.models.company.company.company import Company
    pass  # decoupled: from app.models.company.company.branch import Branch
    pass  # decoupled: from app.models.party.party import Party
    from app.models.purchase.purchase_requisition import PurchaseRequisition
    from app.models.purchase.supplier_quotation import SupplierQuotation
    pass  # decoupled: from app.models.core.currency import Currency
    pass  # decoupled: from app.models.core.address import Address
    from app.models.inventory.warehouse import Warehouse
    pass  # decoupled: from app.models.accounting.payment_term import PaymentTerm
    pass  # decoupled: from app.models.accounting.journal_status import JournalStatus
    pass  # decoupled: from app.models.user.user import User

    from app.models.purchase.purchase_order_item import PurchaseOrderItem
    from app.models.purchase.purchase_receipt import PurchaseReceipt
    from app.models.purchase.purchase_invoice import PurchaseInvoice


class PurchaseOrder(AuditModel):
    """
    Represents an official Purchase Order (PO) issued to a supplier.

    Purpose:
        A Purchase Order is a legally binding commercial document sent to
        a supplier confirming the company's intention to purchase goods or
        services.

        It is normally created from an approved Supplier Quotation or
        Purchase Requisition and becomes the reference document for Goods
        Receipt, Purchase Invoice and Supplier Payments.

    ERP Workflow:

        Purchase Requisition
                │
                ▼
        Request For Quotation
                │
                ▼
        Supplier Quotation
                │
                ▼
            Purchase Order
                │
        ┌───────┴────────┐
        ▼                ▼
    Purchase Receipt  Purchase Invoice
                │
                ▼
            Payment

    Business Benefits:
        - Authorizes purchasing.
        - Creates legal purchasing documents.
        - Tracks supplier commitments.
        - Controls procurement workflow.
        - Enables inventory planning.
        - Supports audit and approvals.

    Relationships:

        Purchase Order
            ├── PurchaseOrderItem
            ├── PurchaseReceipt
            ├── PurchaseInvoice
            └── PurchaseAttachment
    """

    __tablename__ = "purchase_orders"

    purchase_order_no: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
        doc="Unique Purchase Order number.",
    )

    purchase_order_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Date on which the Purchase Order was created.",
    )

    company_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
    )

    branch_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
    )

    supplier_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
    )

    quotation_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("supplier_quotations.id"),
        nullable=True,
        index=True,
    )

    requisition_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("purchase_requisitions.id"),
        nullable=True,
        index=True,
    )

    buyer_id: Mapped[UUID | None] = mapped_column(
        nullable=True,
        index=True,
        doc="Purchasing officer responsible for this order.",
    )

    currency_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
    )

    incoterm_id: Mapped[UUID | None] = mapped_column(
        nullable=True,
        index=True,
    )

    exchange_rate: Mapped[float] = mapped_column(
        Numeric(18, 6),
        nullable=False,
        default=1,
    )

    expected_delivery_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    billing_address_id: Mapped[UUID | None] = mapped_column(
        nullable=True,
    )

    shipping_address_id: Mapped[UUID | None] = mapped_column(
        nullable=True,
    )

    warehouse_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("warehouses.id"),
        nullable=True,
    )

    payment_term_id: Mapped[UUID | None] = mapped_column(
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

    grand_total: Mapped[float] = mapped_column(
        Numeric(18, 2),
        default=0,
    )

    terms_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("purchase_terms.id"),
        nullable=True,
        index=True,
    )

    remarks: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    status_id: Mapped[UUID] = mapped_column(
        nullable=False,
    )

    is_closed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    is_cancelled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    approved_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    approved_by: Mapped[UUID | None] = mapped_column(
        nullable=True,
    )

    # Blanket PO details
    is_blanket: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        doc="Indicates if this is a Blanket Purchase Order.",
    )

    blanket_start_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        doc="Start date for blanket PO validity.",
    )

    blanket_end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        doc="End date for blanket PO validity.",
    )

    blanket_max_amount: Mapped[float | None] = mapped_column(
        Numeric(18, 2),
        nullable=True,
        doc="Maximum value allowed on this blanket PO.",
    )

    blanket_order_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("purchase_orders.id"),
        nullable=True,
        index=True,
        doc="Parent blanket PO if this is a release.",
    )

    # Revision details
    revision_no: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        doc="Revision sequence number of the PO.",
    )

    # Cancellation details
    cancel_reason: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        doc="Reason for order cancellation.",
    )

    cancelled_by_id: Mapped[UUID | None] = mapped_column(
        nullable=True,
        doc="User who cancelled the order.",
    )

    cancelled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp when order was cancelled.",
    )

    # ----------------------------------------------------------
    # Relationships
    # ----------------------------------------------------------




    supplier_quotation: Mapped["SupplierQuotation"] = relationship(
        back_populates="purchase_orders"
    )

    purchase_requisition: Mapped["PurchaseRequisition"] = relationship()






    warehouse: Mapped["Warehouse"] = relationship()



    items: Mapped[list["PurchaseOrderItem"]] = relationship(
        back_populates="purchase_order",
        cascade="all, delete-orphan",
    )

    receipts: Mapped[list["PurchaseReceipt"]] = relationship(
        back_populates="purchase_order",
    )

    invoices: Mapped[list["PurchaseInvoice"]] = relationship(
        back_populates="purchase_order",
    )

    terms: Mapped["PurchaseTerms"] = relationship(
        back_populates="purchase_orders"
    )

    pass  # decoupled: from app.models.core.incoterm import Incoterm


    contract_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("supplier_contracts.id"),
        nullable=True,
        index=True,
    )

    contract: Mapped["SupplierContract"] = relationship(
        back_populates="purchase_orders"
    )

    charges: Mapped[list["PurchaseOrderCharge"]] = relationship(
        back_populates="purchase_order",
        cascade="all, delete-orphan",
    )

    taxes: Mapped[list["PurchaseOrderTax"]] = relationship(
        back_populates="purchase_order",
        cascade="all, delete-orphan",
    )





    revisions: Mapped[list["PurchaseOrderRevision"]] = relationship(
        back_populates="purchase_order",
        cascade="all, delete-orphan",
    )

    blanket_order: Mapped[PurchaseOrder | None] = relationship(
        remote_side="PurchaseOrder.id",
        back_populates="releases",
    )

    releases: Mapped[list[PurchaseOrder]] = relationship(
        back_populates="blanket_order",
    )
