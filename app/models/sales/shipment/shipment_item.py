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
    from app.models.sales.delivery.delivery_note_item import DeliveryNoteItem
    from app.models.sales.shipment.shipment import Shipment


class ShipmentItem(BaseModel):
    """
    Represents an individual Product or Service included in a Shipment.

    Purpose:
        Shipment Item stores every product or service
        transported as part of a Shipment.

        Each Shipment consists of one or more
        Shipment Items.

        Every line records the shipped quantity,
        warehouse,
        packaging information,
        product details,
        shipping status,
        and inventory movement.

        This model forms the basis for warehouse
        dispatch, transportation tracking,
        proof of delivery,
        and shipment reconciliation.

    Examples:

        Shipment

            SHP-2026-000125

        Product

            Dell Latitude Laptop

        Quantity

            20 Nos

        Warehouse

            Main Warehouse

        ------------------------------------

        Product

            Laser Printer

        Quantity

            10 Nos

    Workflow:

            Delivery Note Item
                    │
                    ▼
              Shipment Item
                    │
        ┌───────────┼────────────┐
        ▼           ▼            ▼
    Warehouse   In Transit   Delivered
                    │
                    ▼
           Customer Confirmation

    Benefits:

        • Supports unlimited shipment items.
        • Supports partial shipments.
        • Warehouse integration.
        • Package tracking.
        • Inventory traceability.
        • Proof of delivery.
        • Shipment reconciliation.
        • Complete audit trail.
        • Logistics reporting.
        • Customer shipment tracking.

    Relationships:

              Shipment
                 │
                 ▼
           ShipmentItem
      ┌────────┼────────┬────────┬─────────┐
      ▼        ▼        ▼        ▼
  Product  Variant     UOM   Warehouse

    Example:

        Product

            Dell Latitude 5450

        Quantity

            25

        Warehouse

            Finished Goods Store

    Notes:

        • One Shipment contains multiple items.
        • One Delivery Note Item may generate multiple Shipment Items.
        • Supports partial shipment quantities.
        • Batch allocations are stored separately.
        • Serial numbers are stored separately.
        • Historical values should never change.
        • Used during inventory reconciliation.

    This model is referenced throughout
    Logistics,
    Warehouse,
    Inventory,
    Sales,
    Fleet Management,
    Customer Portal,
    Reporting,
    Analytics,
    and Compliance modules.
    """

    __tablename__ = "shipment_items"

    shipment_id: Mapped[UUID] = mapped_column(
        ForeignKey("shipments.id"),
        nullable=False,
        index=True,
        doc="Reference to the Shipment.",
    )

    delivery_note_item_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("delivery_note_items.id"),
        nullable=True,
        index=True,
        doc="Reference to the originating Delivery Note Item.",
    )

    line_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        doc="Sequential line number within the Shipment.",
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
        doc="Warehouse from which the product is dispatched.",
    )

    uom_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Reference to the Unit of Measure.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Product description printed on the shipment.",
    )

    shipped_quantity: Mapped[Decimal] = mapped_column(
        Numeric(18, 3),
        nullable=False,
        doc="Quantity dispatched in this shipment.",
    )

    delivered_quantity: Mapped[Decimal] = mapped_column(
        Numeric(18, 3),
        nullable=False,
        default=0,
        doc="Quantity successfully delivered.",
    )

    pending_quantity: Mapped[Decimal] = mapped_column(
        Numeric(18, 3),
        nullable=False,
        default=0,
        doc="Remaining quantity pending delivery.",
    )

    package_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
        doc="Number of packages containing this item.",
    )

    gross_weight: Mapped[Decimal] = mapped_column(
        Numeric(18, 3),
        nullable=False,
        default=0,
        doc="Gross weight of the shipment item.",
    )

    net_weight: Mapped[Decimal] = mapped_column(
        Numeric(18, 3),
        nullable=False,
        default=0,
        doc="Net weight of the shipment item.",
    )

    status: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="PENDING",
        doc="Shipment status for this item.",
    )

    remarks: Mapped[str |None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional remarks for this shipment item.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether this shipment item is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    shipment: Mapped["Shipment"] = relationship(
        back_populates="items",
    )

    delivery_note_item: Mapped["DeliveryNoteItem"] = relationship(
        back_populates="shipment_items",
    )




