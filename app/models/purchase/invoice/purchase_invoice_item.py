from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    Numeric,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.inventory.product import Product
    from app.models.inventory.product_variant import ProductVariant
    from app.models.inventory.uom import UOM

    from app.models.purchase.invoice.purchase_invoice import PurchaseInvoice
    from app.models.purchase.order.purchase_order_item import PurchaseOrderItem
    from app.models.purchase.receipt.purchase_receipt_item import PurchaseReceiptItem


class PurchaseInvoiceItem(BaseModel):
    """
    Represents a single line item within a Purchase Invoice.

    Purpose:
        A Purchase Invoice Item records an individual product or service
        billed by the supplier. Each Purchase Invoice may contain one or
        more invoice items.

        Every invoice item maintains complete traceability back to the
        Purchase Order Item and Purchase Receipt Item, enabling
        three-way matching between procurement documents.

    Workflow:

        Purchase Order Item
                │
                ▼
        Purchase Receipt Item
                │
                ▼
        Purchase Invoice Item
                │
                ▼
        Accounts Payable

    Benefits:
        • Supports three-way matching.
        • Tracks supplier billed quantities.
        • Maintains pricing history.
        • Calculates taxes and discounts.
        • Supports Accounts Payable.
        • Complete financial audit trail.

    Relationships:

        PurchaseInvoice
                │
                └── PurchaseInvoiceItem

        PurchaseOrderItem
                │
                └── PurchaseInvoiceItem

        PurchaseReceiptItem
                │
                └── PurchaseInvoiceItem

        Product
                │
                └── PurchaseInvoiceItem

        ProductVariant
                │
                └── PurchaseInvoiceItem

        UOM
                │
                └── PurchaseInvoiceItem
    """

    __tablename__ = "purchase_invoice_items"

    purchase_invoice_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_invoices.id"),
        nullable=False,
        index=True,
        doc="Reference to the Purchase Invoice.",
    )

    purchase_order_item_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("purchase_order_items.id"),
        nullable=True,
        index=True,
        doc="Reference to the Purchase Order Item.",
    )

    purchase_receipt_item_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("purchase_receipt_items.id"),
        nullable=True,
        index=True,
        doc="Reference to the Purchase Receipt Item.",
    )

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
        doc="Purchased product.",
    )

    variant_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("product_variants.id"),
        nullable=True,
        index=True,
        doc="Purchased product variant.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional description for the invoice item.",
    )

    uom_id: Mapped[UUID] = mapped_column(
        ForeignKey("uoms.id"),
        nullable=False,
        index=True,
        doc="Unit of Measure.",
    )

    received_quantity: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        doc="Quantity received from the supplier.",
    )

    invoiced_quantity: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        doc="Quantity billed by the supplier.",
    )

    unit_price: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        doc="Supplier unit price.",
    )

    discount_percentage: Mapped[float] = mapped_column(
        Numeric(8, 2),
        nullable=False,
        default=0,
        doc="Discount percentage.",
    )

    discount_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Discount amount.",
    )

    tax_percentage: Mapped[float] = mapped_column(
        Numeric(8, 2),
        nullable=False,
        default=0,
        doc="Tax percentage.",
    )

    tax_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Tax amount.",
    )

    line_total: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Net invoice amount for this line.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional remarks.",
    )

    line_no: Mapped[int] = mapped_column(
        nullable=False,
        doc="Line number within the Purchase Invoice.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    purchase_invoice: Mapped["PurchaseInvoice"] = relationship(
        back_populates="items",
    )

    purchase_order_item: Mapped["PurchaseOrderItem"] = relationship()

    purchase_receipt_item: Mapped["PurchaseReceiptItem"] = relationship()

    product: Mapped["Product"] = relationship()

    variant: Mapped["ProductVariant"] = relationship()

    uom: Mapped["UOM"] = relationship()

    taxes: Mapped[list["PurchaseInvoiceItemTax"]] = relationship(
        back_populates="purchase_invoice_item",
        cascade="all, delete-orphan",
    )