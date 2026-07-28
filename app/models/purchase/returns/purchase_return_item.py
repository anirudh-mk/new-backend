from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.inventory.product import Product
    from app.models.inventory.product_variant import ProductVariant
    from app.models.inventory.uom import UOM

    from app.models.purchase.returns.purchase_return import PurchaseReturn
    from app.models.purchase.receipt.purchase_receipt_item import PurchaseReceiptItem
    from app.models.purchase.invoice.purchase_invoice_item import PurchaseInvoiceItem


class PurchaseReturnItem(BaseModel):
    """
    Represents a single product returned to a supplier.

    Purpose:
        A Purchase Return Item records an individual product line that
        is being returned to the supplier. Every Purchase Return may
        contain one or more return items.

        The item maintains complete traceability back to the Purchase
        Receipt Item and Purchase Invoice Item while recording the
        returned quantity and financial impact.

    Workflow:

        Purchase Receipt
                │
                ▼
        Purchase Receipt Item
                │
                ▼
        Purchase Return
                │
                ▼
        Purchase Return Item
                │
                ▼
        Supplier Credit / AP Adjustment

    Benefits:
        • Tracks returned quantities.
        • Maintains inventory traceability.
        • Supports supplier credit notes.
        • Preserves pricing information.
        • Supports item-level reporting.
        • Complete audit history.

    Relationships:

        PurchaseReturn
                │
                └── PurchaseReturnItem

        PurchaseReceiptItem
                │
                └── PurchaseReturnItem

        PurchaseInvoiceItem
                │
                └── PurchaseReturnItem

        Product
                │
                └── PurchaseReturnItem

        ProductVariant
                │
                └── PurchaseReturnItem

        UOM
                │
                └── PurchaseReturnItem
    """

    __tablename__ = "purchase_return_items"

    purchase_return_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_returns.id"),
        nullable=False,
        index=True,
        doc="Reference to the Purchase Return.",
    )

    purchase_receipt_item_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_receipt_items.id"),
        nullable=False,
        index=True,
        doc="Reference to the original Purchase Receipt Item.",
    )

    purchase_invoice_item_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("purchase_invoice_items.id"),
        nullable=True,
        index=True,
        doc="Reference to the Purchase Invoice Item.",
    )

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
        doc="Returned product.",
    )

    variant_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("product_variants.id"),
        nullable=True,
        index=True,
        doc="Returned product variant.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional description for the returned item.",
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
        doc="Original received quantity.",
    )

    returned_quantity: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        doc="Quantity returned to the supplier.",
    )

    unit_price: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        doc="Unit purchase price.",
    )

    discount_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Discount amount for this item.",
    )

    tax_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Tax amount for this item.",
    )

    line_total: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Net return value for this item.",
    )

    reason: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        doc="Reason for returning this item.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional remarks.",
    )

    line_no: Mapped[int] = mapped_column(
        nullable=False,
        doc="Line number within the Purchase Return document.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    purchase_return: Mapped["PurchaseReturn"] = relationship(
        back_populates="items",
    )

    purchase_receipt_item: Mapped["PurchaseReceiptItem"] = relationship()

    purchase_invoice_item: Mapped["PurchaseInvoiceItem"] = relationship()

    product: Mapped["Product"] = relationship()

    variant: Mapped["ProductVariant"] = relationship()

    uom: Mapped["UOM"] = relationship()