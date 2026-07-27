from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Date,
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
    from app.models.purchase.purchase_requisition import PurchaseRequisition
    from app.models.purchase.supplier_quotation import SupplierQuotation
    from app.models.common.currency import Currency
    from app.models.common.address import Address
    from app.models.inventory.warehouse import Warehouse
    from app.models.accounting.payment_term import PaymentTerm
    from app.models.accounting.journal_status import JournalStatus
    from app.models.user.user import User

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

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
    )

    branch_id: Mapped[int] = mapped_column(
        ForeignKey("branches.id"),
        nullable=False,
        index=True,
    )

    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("parties.id"),
        nullable=False,
        index=True,
    )

    quotation_id: Mapped[int | None] = mapped_column(
        ForeignKey("supplier_quotations.id"),
        nullable=True,
        index=True,
    )

    requisition_id: Mapped[int | None] = mapped_column(
        ForeignKey("purchase_requisitions.id"),
        nullable=True,
        index=True,
    )

    buyer_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True,
        doc="Purchasing officer responsible for this order.",
    )

    currency_id: Mapped[int] = mapped_column(
        ForeignKey("currencies.id"),
        nullable=False,
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

    billing_address_id: Mapped[int | None] = mapped_column(
        ForeignKey("addresses.id"),
        nullable=True,
    )

    shipping_address_id: Mapped[int | None] = mapped_column(
        ForeignKey("addresses.id"),
        nullable=True,
    )

    warehouse_id: Mapped[int | None] = mapped_column(
        ForeignKey("warehouses.id"),
        nullable=True,
    )

    payment_term_id: Mapped[int | None] = mapped_column(
        ForeignKey("payment_terms.id"),
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

    remarks: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    status_id: Mapped[int] = mapped_column(
        ForeignKey("journal_statuses.id"),
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

    approved_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    # ----------------------------------------------------------
    # Relationships
    # ----------------------------------------------------------

    company: Mapped["Company"] = relationship()

    branch: Mapped["Branch"] = relationship()

    supplier: Mapped["Party"] = relationship()

    supplier_quotation: Mapped["SupplierQuotation"] = relationship(
        back_populates="purchase_orders"
    )

    purchase_requisition: Mapped["PurchaseRequisition"] = relationship()

    buyer: Mapped["User"] = relationship(
        foreign_keys=[buyer_id]
    )

    approver: Mapped["User"] = relationship(
        foreign_keys=[approved_by]
    )

    currency: Mapped["Currency"] = relationship()

    billing_address: Mapped["Address"] = relationship(
        foreign_keys=[billing_address_id]
    )

    shipping_address: Mapped["Address"] = relationship(
        foreign_keys=[shipping_address_id]
    )

    warehouse: Mapped["Warehouse"] = relationship()

    payment_term: Mapped["PaymentTerm"] = relationship()

    status: Mapped["JournalStatus"] = relationship()

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