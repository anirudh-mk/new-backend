from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.inventory.product.product import Product
    from app.models.inventory.product.product_variant import ProductVariant
    from app.models.inventory.stock.batch import Batch
    from app.models.inventory.stock.serial_number import SerialNumber
    from app.models.inventory.stock.stock import Stock
    from app.models.inventory.warehouse.warehouse import Warehouse
    from app.models.inventory.warehouse.warehouse_location import WarehouseLocation


class StockReservation(BaseModel):
    """
    Represents inventory reserved for a future business transaction.

    Purpose:
        Stock Reservation temporarily allocates inventory to a business
        document without physically removing it from inventory.

        Reserved inventory remains physically available in the warehouse
        but cannot be allocated to another transaction until the
        reservation is released or fulfilled.

        Stock Reservations are commonly created from:

            • Sales Orders
            • Manufacturing Orders
            • Transfer Orders
            • Service Orders
            • Project Allocations

        Once the inventory movement occurs, the reservation is released
        and a StockTransaction records the physical movement.

    Workflow:

            Sales Order
                  │
                  ▼
           Stock Reservation
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
    Reserved Qty      Available Qty
                            │
                            ▼
                    Delivery Note
                            │
                            ▼
                    Stock Transaction
                            │
                            ▼
                   Reservation Released

    Example:

        Current Stock

            On Hand

                100

            Reserved

                25

            Available

                75

    Benefits:

        • Prevents double allocation.
        • Supports order fulfillment.
        • Supports manufacturing allocation.
        • Supports warehouse picking.
        • Supports inventory planning.
        • Improves stock availability accuracy.
        • Enables reservation history.
        • Supports partial deliveries.
        • Improves customer commitment.

    Relationships:

                    Warehouse
                        │
                        ▼
                 Warehouse Location
                        │
                        ▼
                Stock Reservation
            ┌───────────┼────────────┐
            ▼           ▼            ▼
        Product      Variant      Batch
                                        │
                                        ▼
                                 Serial Number

    Reservation Sources:

        Sales Order

        Manufacturing Order

        Stock Transfer

        Project

        Service Order

    Reservation States:

        Reserved

        Released

        Fulfilled

        Cancelled

    Notes:

        • Reservation does NOT reduce On Hand inventory.
        • Reservation reduces Available inventory.
        • Reservations should always originate from
          a business transaction.
        • Fulfillment creates Stock Transactions.
        • Reservations should never exist without
          a valid source document.

    This model is referenced throughout
    Inventory,
    Warehouse,
    Sales,
    Manufacturing,
    MRP,
    Logistics,
    POS,
    and Reporting modules.
    """

    __tablename__ = "stock_reservations"

    stock_id: Mapped[UUID] = mapped_column(
        ForeignKey("stock.id"),
        nullable=False,
        index=True,
        doc="Reference to the current stock record.",
    )

    warehouse_id: Mapped[UUID] = mapped_column(
        ForeignKey("warehouses.id"),
        nullable=False,
        index=True,
        doc="Warehouse containing the reserved inventory.",
    )

    warehouse_location_id: Mapped[UUID] = mapped_column(
        ForeignKey("warehouse_locations.id"),
        nullable=False,
        index=True,
        doc="Warehouse Location containing the reserved inventory.",
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

    batch_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("batches.id"),
        nullable=True,
        index=True,
    )

    serial_number_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("serial_numbers.id"),
        nullable=True,
        index=True,
    )

    reference_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        doc="Business document creating the reservation.",
    )

    reference_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Primary key of the originating business document.",
    )

    reserved_quantity: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        doc="Quantity currently reserved.",
    )

    reservation_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        doc="Date and time when inventory was reserved.",
    )

    expiry_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        doc="Optional reservation expiry date.",
    )

    is_released: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether the reservation has been released.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional reservation remarks.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    stock: Mapped["Stock"] = relationship()

    warehouse: Mapped["Warehouse"] = relationship()

    warehouse_location: Mapped["WarehouseLocation"] = relationship()

    product: Mapped["Product"] = relationship()

    variant: Mapped["ProductVariant | None"] = relationship()

    batch: Mapped["Batch | None"] = relationship()

    serial_number: Mapped["SerialNumber | None"] = relationship()