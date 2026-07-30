from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    Numeric,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.inventory.stock.batch import Batch
    from app.models.inventory.product.product import Product
    from app.models.inventory.product.product_variant import ProductVariant
    from app.models.inventory.stock.serial_number import SerialNumber
    from app.models.inventory.warehouse.warehouse import Warehouse
    from app.models.inventory.warehouse.warehouse_location import WarehouseLocation


class Stock(BaseModel):
    """
    Represents the current inventory balance of a Product Variant
    stored at a specific Warehouse Location.

    Purpose:
        Stock maintains the current inventory snapshot for every
        unique inventory combination within the ERP.

        Unlike StockTransaction, which records every inventory
        movement, the Stock model stores only the latest inventory
        balance for fast inventory lookups.

        Every inventory movement updates this table while the
        detailed audit history remains in StockTransaction.

    Inventory Key:

        Warehouse
            +
        Warehouse Location
            +
        Product
            +
        Product Variant
            +
        Batch (Optional)
            +
        Serial Number (Optional)

    Example:

        Main Warehouse

            Rack A1

                Dell Laptop
                    Black / 16GB

                    Batch
                        B001

                    Quantity

                        On Hand      25
                        Reserved      5
                        Available    20

    Workflow:

                Purchase Receipt
                        │
                        ▼
                Stock Transaction
                        │
                        ▼
                    Stock Update
                        │
        ┌───────────────┼──────────────┐
        ▼               ▼              ▼
     Purchase        Sales        Transfer
                        │
                        ▼
                   Manufacturing

    Benefits:

        • Fast inventory lookup.
        • Warehouse-wise stock.
        • Bin-wise stock.
        • Batch-wise inventory.
        • Serial-wise inventory.
        • Reserved quantity tracking.
        • Available quantity calculation.
        • Inventory valuation support.
        • Real-time stock availability.

    Relationships:

                    Warehouse
                        │
                        ▼
                 Warehouse Location
                        │
                        ▼
                      Stock
                ┌───────┼─────────┐
                ▼       ▼         ▼
            Product   Variant    Batch
                                     │
                                     ▼
                              Serial Number

    Quantity Definitions:

        On Hand

            Physical inventory currently stored.

        Reserved

            Inventory allocated to Sales Orders,
            Manufacturing Orders, etc.

        Available

            On Hand - Reserved

        Incoming

            Expected inventory from Purchase Orders.

        Outgoing

            Expected inventory committed to customers.

    Notes:

        • Stock represents the current balance only.
        • Historical movements belong in StockTransaction.
        • Inventory should never be manually adjusted here.
        • Every update should originate from a business transaction.
        • Available Quantity should never become negative unless
          negative inventory is permitted.

    This model is referenced throughout Inventory,
    Warehouse,
    Purchase,
    Sales,
    Manufacturing,
    POS,
    MRP,
    Logistics,
    and Reporting modules.
    """

    __tablename__ = "stock"

    warehouse_id: Mapped[UUID] = mapped_column(
        ForeignKey("warehouses.id"),
        nullable=False,
        index=True,
        doc="Warehouse storing the inventory.",
    )

    warehouse_location_id: Mapped[UUID] = mapped_column(
        ForeignKey("warehouse_locations.id"),
        nullable=False,
        index=True,
        doc="Warehouse Location where inventory is stored.",
    )

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
        doc="Reference to the Product.",
    )

    variant_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("product_variants.id"),
        nullable=True,
        index=True,
        doc="Reference to the Product Variant.",
    )

    batch_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("batches.id"),
        nullable=True,
        index=True,
        doc="Inventory batch.",
    )

    serial_number_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("serial_numbers.id"),
        nullable=True,
        index=True,
        doc="Serial number when serial tracking is enabled.",
    )

    on_hand_quantity: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        default=0,
        doc="Physical quantity currently available in the warehouse.",
    )

    reserved_quantity: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        default=0,
        doc="Quantity reserved for pending business transactions.",
    )

    available_quantity: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        default=0,
        doc="Quantity available for new transactions.",
    )

    incoming_quantity: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        default=0,
        doc="Expected incoming quantity from open Purchase Orders or Transfers.",
    )

    outgoing_quantity: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        default=0,
        doc="Expected outgoing quantity committed to customers or transfers.",
    )

    average_cost: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        default=0,
        doc="Current weighted average inventory cost.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    warehouse: Mapped["Warehouse"] = relationship(
        back_populates="stock",
    )

    warehouse_location: Mapped["WarehouseLocation"] = relationship(
        back_populates="stock",
    )

    product: Mapped["Product"] = relationship()

    variant: Mapped["ProductVariant | None"] = relationship(
        back_populates="stock",
    )

    batch: Mapped["Batch | None"] = relationship()

    serial_number: Mapped["SerialNumber | None"] = relationship()
