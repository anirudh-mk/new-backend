from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Date,
    ForeignKey,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel, BaseModel

if TYPE_CHECKING:
    from app.models.company.company import Company
    from app.models.company.branch import Branch
    from app.models.party.party import Party
    from app.models.purchase.receipt.purchase_receipt import PurchaseReceipt
    from app.models.purchase.order.purchase_order import PurchaseOrder
    from app.models.user.user import User
    from app.models.accounting.journal_status import JournalStatus
    from app.models.purchase.receipt.purchase_receipt_item import PurchaseReceiptItem
    from app.models.purchase.order.purchase_order_item import PurchaseOrderItem
    from app.models.inventory.product import Product
    from app.models.inventory.product_variant import ProductVariant
    from app.models.inventory.uom import UOM


class RejectedReceipt(AuditModel):
    """
    Represents a document detailing goods rejected at receipt before inventory update.
    """

    __tablename__ = "rejected_receipts"

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

    supplier_id: Mapped[UUID] = mapped_column(
        ForeignKey("parties.id"),
        nullable=False,
        index=True,
    )

    purchase_receipt_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("purchase_receipts.id"),
        nullable=True,
        index=True,
        doc="Reference to the linked Goods Receipt if any.",
    )

    purchase_order_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("purchase_orders.id"),
        nullable=True,
        index=True,
        doc="Reference to the originating Purchase Order if any.",
    )

    rejection_no: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
        doc="Unique Rejection Note number.",
    )

    rejection_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Date on which goods were rejected.",
    )

    rejected_by_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
        doc="User who logged the rejection.",
    )

    status_id: Mapped[UUID] = mapped_column(
        ForeignKey("journal_statuses.id"),
        nullable=False,
        index=True,
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Relationships
    company: Mapped["Company"] = relationship()
    branch: Mapped["Branch"] = relationship()
    supplier: Mapped["Party"] = relationship()
    purchase_receipt: Mapped["PurchaseReceipt"] = relationship()
    purchase_order: Mapped["PurchaseOrder"] = relationship()
    rejected_by: Mapped["User"] = relationship(foreign_keys=[rejected_by_id])
    status: Mapped["JournalStatus"] = relationship()

    items: Mapped[list["RejectedReceiptItem"]] = relationship(
        back_populates="rejected_receipt",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<RejectedReceipt(rejection_no='{self.rejection_no}', date='{self.rejection_date}')>"


class RejectedReceiptItem(BaseModel):
    """
    Represents an item rejected at receipt.
    """

    __tablename__ = "rejected_receipt_items"

    rejected_receipt_id: Mapped[UUID] = mapped_column(
        ForeignKey("rejected_receipts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    purchase_receipt_item_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("purchase_receipt_items.id"),
        nullable=True,
        index=True,
    )

    purchase_order_item_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("purchase_order_items.id"),
        nullable=True,
        index=True,
    )

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )

    variant_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("product_variants.id"),
        nullable=True,
        index=True,
    )

    uom_id: Mapped[UUID] = mapped_column(
        ForeignKey("uoms.id"),
        nullable=False,
        index=True,
    )

    rejected_quantity: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        doc="Quantity rejected.",
    )

    unit_price: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
    )

    rejection_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Detailed reason for rejecting the item.",
    )

    line_no: Mapped[int] = mapped_column(
        nullable=False,
    )

    # Relationships
    rejected_receipt: Mapped["RejectedReceipt"] = relationship(back_populates="items")
    purchase_receipt_item: Mapped["PurchaseReceiptItem"] = relationship()
    purchase_order_item: Mapped["PurchaseOrderItem"] = relationship()
    product: Mapped["Product"] = relationship()
    variant: Mapped["ProductVariant"] = relationship()
    uom: Mapped["UOM"] = relationship()

    def __repr__(self) -> str:
        return f"<RejectedReceiptItem(rejected_receipt_id='{self.rejected_receipt_id}', qty={self.rejected_quantity})>"
