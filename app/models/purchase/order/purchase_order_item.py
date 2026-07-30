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

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.inventory.product.product import Product
    from app.models.inventory.product.product_variant import ProductVariant
    from app.models.inventory.uom.uom import UOM

    from app.models.purchase.order.purchase_order import PurchaseOrder
    from app.models.purchase.quotation.supplier_quotation_item import SupplierQuotationItem


class PurchaseOrderItem(BaseModel):
    """
    Represents a single line item within a Purchase Order.

    Purpose:
        A Purchase Order Item records an individual product or service
        being purchased from a supplier. Each Purchase Order can contain
        multiple items with their own quantities, pricing, taxes,
        discounts, and delivery dates.

        The item maintains complete traceability from the accepted
        Supplier Quotation through Goods Receipt, Purchase Invoice,
        and Purchase Return.

    Workflow:

        Supplier Quotation Item
                │
                ▼
        Purchase Order Item
          │        │        │
          ▼        ▼        ▼
      Purchase   Purchase   Purchase
      Receipt    Invoice    Return

    Benefits:
        • Tracks ordered quantities.
        • Tracks received quantities.
        • Tracks invoiced quantities.
        • Supports partial deliveries.
        • Maintains pricing history.
        • Supports procurement analytics.
        • Complete audit trail.

    Relationships:

        PurchaseOrder
                │
                └── PurchaseOrderItem

        SupplierQuotationItem
                │
                └── PurchaseOrderItem

        Product
                │
                └── PurchaseOrderItem

        ProductVariant
                │
                └── PurchaseOrderItem

        UOM
                │
                └── PurchaseOrderItem
    """

    __tablename__ = "purchase_order_items"

    purchase_order_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_orders.id"),
        nullable=False,
        index=True,
        doc="Reference to the Purchase Order.",
    )

    supplier_quotation_item_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("supplier_quotation_items.id"),
        nullable=True,
        index=True,
        doc="Reference to the accepted Supplier Quotation Item.",
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
        doc="Additional description for the purchased item.",
    )

    uom_id: Mapped[UUID] = mapped_column(
        ForeignKey("uoms.id"),
        nullable=False,
        index=True,
        doc="Unit of Measure.",
    )

    ordered_quantity: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        doc="Quantity ordered from the supplier.",
    )

    received_quantity: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        default=0,
        doc="Total quantity received.",
    )

    invoiced_quantity: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        default=0,
        doc="Total quantity invoiced by the supplier.",
    )

    remaining_quantity: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        default=0,
        doc="Remaining quantity yet to be received.",
    )

    unit_price: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        doc="Purchase unit price.",
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
        doc="Net line amount after discount and tax.",
    )

    expected_delivery_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        doc="Expected delivery date for this item.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional remarks.",
    )

    line_no: Mapped[int] = mapped_column(
        nullable=False,
        doc="Line number within the Purchase Order.",
    )

    blanket_order_item_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("purchase_order_items.id"),
        nullable=True,
        index=True,
        doc="Parent blanket PO line item if this is a release.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    purchase_order: Mapped["PurchaseOrder"] = relationship(
        back_populates="items",
    )

    supplier_quotation_item: Mapped["SupplierQuotationItem"] = relationship()

    product: Mapped["Product"] = relationship()

    variant: Mapped["ProductVariant"] = relationship()

    uom: Mapped["UOM"] = relationship()

    blanket_order_item: Mapped[PurchaseOrderItem | None] = relationship(
        remote_side="PurchaseOrderItem.id",
        back_populates="release_items",
    )

    release_items: Mapped[list[PurchaseOrderItem]] = relationship(
        back_populates="blanket_order_item",
    )

    taxes: Mapped[list["PurchaseOrderItemTax"]] = relationship(
        back_populates="purchase_order_item",
        cascade="all, delete-orphan",
    )