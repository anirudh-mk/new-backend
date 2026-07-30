from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    Numeric,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.sales.delivery.delivery_note import DeliveryNote
    from app.models.sales.order.sales_order_item import SalesOrderItem


class DeliveryNoteItem(BaseModel):
    """
    Represents an individual Product or Service delivered to a Customer.

    Purpose:
        Delivery Note Item represents each product or service
        physically delivered under a Delivery Note.

        Every Delivery Note consists of one or more line items.

        Each item stores the delivered quantity,
        warehouse allocation,
        pricing snapshot,
        taxes,
        serial numbers,
        batch allocation,
        and delivery status.

        It serves as the bridge between
        Sales Orders,
        Warehouse Operations,
        Inventory,
        Logistics,
        and Customer Delivery.

    Examples:

        Delivery Note

            DN-2026-000125

        Item

            Dell Latitude Laptop

        Ordered Qty

            20

        Delivered Qty

            15

        Remaining Qty

            5

        -------------------------------------

        Product

            Printer

        Delivered

            10 Nos

    Workflow:

              Sales Order Item
                      │
                      ▼
            Delivery Note Item
                      │
        ┌─────────────┼──────────────┐
        ▼             ▼              ▼
    Batch Allocation Serial Number Warehouse
                      │
                      ▼
              Inventory Reduction
                      │
                      ▼
                Sales Invoice

    Benefits:

        • Supports partial deliveries.
        • Warehouse allocation.
        • Inventory deduction.
        • Batch tracking.
        • Serial number tracking.
        • Delivery status tracking.
        • Pricing snapshot.
        • Audit trail.
        • Customer fulfillment tracking.
        • Logistics integration.

    Relationships:

            DeliveryNote
                 │
                 ▼
          DeliveryNoteItem
        ┌────────┼────────┬─────────┬─────────┐
        ▼        ▼        ▼         ▼
    Product  Variant     UOM   Warehouse

    Example:

        Product

            Dell Latitude 5450

        Warehouse

            Main Warehouse

        Delivered Qty

            12

        Status

            Delivered

    Notes:

        • One Delivery Note contains many items.
        • One Sales Order Item may generate multiple Delivery Items.
        • Supports partial deliveries.
        • Taxes are stored separately.
        • Batch information is stored separately.
        • Serial numbers are stored separately.
        • Historical records should never change.
        • Used during invoice creation.

    This model is referenced throughout
    Sales,
    Inventory,
    Warehouse,
    Logistics,
    Shipping,
    Accounting,
    Reporting,
    Analytics,
    and Supply Chain modules.
    """

    __tablename__ = "delivery_note_items"

    delivery_note_id: Mapped[UUID] = mapped_column(
        ForeignKey("delivery_notes.id"),
        nullable=False,
        index=True,
        doc="Reference to the Delivery Note.",
    )

    sales_order_item_id: Mapped[UUID] = mapped_column(
        ForeignKey("sales_order_items.id"),
        nullable=False,
        index=True,
        doc="Reference to the originating Sales Order Item.",
    )

    line_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        doc="Sequential line number within the Delivery Note.",
    )

    product_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Reference to the Product.",
    )

    product_variant_id: Mapped[UUID | None] = mapped_column(
        nullable=True,
        index=True,
        doc="Reference to the Product Variant.",
    )

    warehouse_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Warehouse from which the product was delivered.",
    )

    uom_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Reference to the Unit of Measure.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Product description printed on the Delivery Note.",
    )

    ordered_quantity: Mapped[Decimal] = mapped_column(
        Numeric(18, 3),
        nullable=False,
        doc="Original ordered quantity.",
    )

    delivered_quantity: Mapped[Decimal] = mapped_column(
        Numeric(18, 3),
        nullable=False,
        doc="Quantity delivered in this Delivery Note.",
    )

    remaining_quantity: Mapped[Decimal] = mapped_column(
        Numeric(18, 3),
        nullable=False,
        default=0,
        doc="Remaining quantity yet to be delivered.",
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Selling price snapshot at delivery time.",
    )

    discount_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Discount applied to this delivery item.",
    )

    tax_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Total tax amount for this item.",
    )

    net_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Final amount after taxes and discounts.",
    )

    delivery_status: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="DELIVERED",
        doc="Current delivery status of the item.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional remarks for this delivery item.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether this delivery item is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    delivery_note: Mapped["DeliveryNote"] = relationship(
        back_populates="items",
    )

    sales_order_item: Mapped["SalesOrderItem"] = relationship(
        back_populates="delivery_items",
    )




