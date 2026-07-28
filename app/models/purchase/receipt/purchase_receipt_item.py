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
    from app.models.inventory.product import Product
    from app.models.inventory.product_variant import ProductVariant
    from app.models.inventory.uom import UOM
    from app.models.inventory.warehouse_location import WarehouseLocation

    from app.models.purchase.receipt.purchase_receipt import PurchaseReceipt
    from app.models.purchase.order.purchase_order_item import PurchaseOrderItem


class PurchaseReceiptItem(BaseModel):
    """
    Represents an individual item received from a supplier.

    Purpose:
        Purchase Receipt Item records each product received against a
        Purchase Order. It maintains the actual received quantity,
        accepted quantity, rejected quantity, warehouse location,
        batch details and serial numbers.

        These records are used for inventory updates, quality inspection,
        landed cost allocation, purchase invoice verification and
        supplier returns.

    Workflow:

        Purchase Order Item
                │
                ▼
        Purchase Receipt
                │
                ▼
        Purchase Receipt Item
          │      │       │
          ▼      ▼       ▼
      Inventory  Invoice  Purchase Return

    Benefits:
        • Updates inventory.
        • Supports partial receipts.
        • Supports quality inspection.
        • Supports batch tracking.
        • Supports serial tracking.
        • Enables landed cost allocation.
        • Complete inventory audit trail.

    Relationships:

        PurchaseReceipt
                │
                └── PurchaseReceiptItem

        PurchaseOrderItem
                │
                └── PurchaseReceiptItem

        Product
                │
                └── PurchaseReceiptItem

        ProductVariant
                │
                └── PurchaseReceiptItem

        UOM
                │
                └── PurchaseReceiptItem

        WarehouseLocation
                │
                └── PurchaseReceiptItem
    """

    __tablename__ = "purchase_receipt_items"

    purchase_receipt_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_receipts.id"),
        nullable=False,
        index=True,
        doc="Reference to the Purchase Receipt.",
    )

    purchase_order_item_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_order_items.id"),
        nullable=False,
        index=True,
        doc="Reference to the Purchase Order Item.",
    )

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
        doc="Received product.",
    )

    variant_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("product_variants.id"),
        nullable=True,
        index=True,
        doc="Product variant.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional description.",
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
        doc="Quantity ordered.",
    )

    received_quantity: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        doc="Quantity received.",
    )

    accepted_quantity: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        default=0,
        doc="Quantity accepted into inventory.",
    )

    rejected_quantity: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        default=0,
        doc="Quantity rejected.",
    )

    unit_price: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        doc="Purchase unit price.",
    )

    discount_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Discount amount.",
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
        doc="Total amount for this line.",
    )

    warehouse_location_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("warehouse_locations.id"),
        nullable=True,
        index=True,
        doc="Warehouse bin/rack/shelf.",
    )

    # Import and shipment specific fields
    manufacturing_batch: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        doc="Batch reference from manufacturer.",
    )

    country_of_origin: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        doc="Country where the goods were produced.",
    )

    container_no: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        doc="Shipping container number (for imports).",
    )

    seal_no: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        doc="Customs/security seal number.",
    )

    batch_no: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        doc="Batch or lot number.",
    )

    serial_no: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        doc="Serial number.",
    )

    manufacturing_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        doc="Manufacturing date.",
    )

    expiry_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        doc="Expiry date.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional remarks.",
    )

    line_no: Mapped[int] = mapped_column(
        nullable=False,
        doc="Line number within the Purchase Receipt.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    purchase_receipt: Mapped["PurchaseReceipt"] = relationship(
        back_populates="items",
    )

    purchase_order_item: Mapped["PurchaseOrderItem"] = relationship()

    product: Mapped["Product"] = relationship()

    variant: Mapped["ProductVariant"] = relationship()

    uom: Mapped["UOM"] = relationship()

    warehouse_location: Mapped["WarehouseLocation"] = relationship()