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
    from app.models.inventory.product.product import Product
    from app.models.inventory.product.product_variant import ProductVariant
    from app.models.inventory.uom.uom import UOM
    from app.models.inventory.warehouse.warehouse import Warehouse
    from app.models.sales.order.sales_order import SalesOrder
    from app.models.sales.quotation.sales_quotation_item import SalesQuotationItem


class SalesOrderItem(BaseModel):
    """
    Represents an individual Product or Service within a Sales Order.

    Purpose:
        Sales Order Item stores the individual products or services
        ordered by a customer.

        Each Sales Order consists of one or more Sales Order Items.

        Every item maintains product information,
        ordered quantity,
        delivered quantity,
        invoiced quantity,
        pricing,
        discounts,
        taxes,
        warehouse allocation,
        and fulfillment status.

        This model is the operational bridge between
        Sales, Inventory, Warehouse,
        Delivery, Manufacturing,
        and Accounting.

    Examples:

        Sales Order

            SO-000125

        Item

            Dell Latitude Laptop

        Ordered

            10 Nos

        Delivered

            4 Nos

        Remaining

            6 Nos

        ------------------------------------

        Product

            Printer

        Qty

            20

        Warehouse

            Main Warehouse

    Workflow:

              Sales Order
                    │
                    ▼
             Sales Order Item
                    │
        ┌───────────┼────────────┐
        ▼           ▼            ▼
    Reservation Delivery      Invoice
        │           │            │
        ▼           ▼            ▼
     Inventory   Warehouse   Accounting

    Benefits:

        • Supports unlimited order lines.
        • Product variant support.
        • Warehouse allocation.
        • Partial delivery support.
        • Partial invoicing support.
        • Quantity tracking.
        • Margin analysis.
        • Inventory reservation.
        • Manufacturing integration.
        • Complete traceability.

    Relationships:

               SalesOrder
                    │
                    ▼
             SalesOrderItem
        ┌────────┼─────────┬─────────┐
        ▼        ▼         ▼         ▼
    Product  Variant     UOM    Warehouse

    Example:

        Product

            Dell Latitude 5450

        Variant

            i7 / 16GB / 512GB

        Warehouse

            Main Warehouse

        Ordered Qty

            15

        Delivered Qty

            10

        Remaining Qty

            5

    Notes:

        • One Sales Order contains many items.
        • Items may be partially delivered.
        • Items may be partially invoiced.
        • Taxes are maintained separately.
        • Charges are maintained separately.
        • Batch allocation is maintained separately.
        • Serial numbers are maintained separately.
        • Historical records should never change.

    This model is referenced throughout
    Sales,
    Inventory,
    Warehouse,
    Delivery,
    Manufacturing,
    Accounting,
    Procurement,
    Reporting,
    Analytics,
    and Customer Portal modules.
    """

    __tablename__ = "sales_order_items"

    sales_order_id: Mapped[UUID] = mapped_column(
        ForeignKey("sales_orders.id"),
        nullable=False,
        index=True,
        doc="Reference to the Sales Order.",
    )

    quotation_item_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("sales_quotation_items.id"),
        nullable=True,
        index=True,
        doc="Reference to the originating Sales Quotation Item.",
    )

    line_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        doc="Sequential line number within the Sales Order.",
    )

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
        doc="Reference to the Product.",
    )

    product_variant_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("product_variants.id"),
        nullable=True,
        index=True,
        doc="Reference to the Product Variant.",
    )

    warehouse_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("warehouses.id"),
        nullable=True,
        index=True,
        doc="Warehouse from which the product will be supplied.",
    )

    uom_id: Mapped[UUID] = mapped_column(
        ForeignKey("uoms.id"),
        nullable=False,
        index=True,
        doc="Unit of Measure.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Product description printed on the Sales Order.",
    )

    ordered_quantity: Mapped[Decimal] = mapped_column(
        Numeric(18, 3),
        nullable=False,
        default=1,
        doc="Quantity ordered by the customer.",
    )

    delivered_quantity: Mapped[Decimal] = mapped_column(
        Numeric(18, 3),
        nullable=False,
        default=0,
        doc="Quantity already delivered.",
    )

    invoiced_quantity: Mapped[Decimal] = mapped_column(
        Numeric(18, 3),
        nullable=False,
        default=0,
        doc="Quantity already invoiced.",
    )

    reserved_quantity: Mapped[Decimal] = mapped_column(
        Numeric(18, 3),
        nullable=False,
        default=0,
        doc="Inventory quantity reserved for this order.",
    )

    cancelled_quantity: Mapped[Decimal] = mapped_column(
        Numeric(18, 3),
        nullable=False,
        default=0,
        doc="Cancelled quantity.",
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Selling price per unit.",
    )

    discount_percentage: Mapped[Decimal] = mapped_column(
        Numeric(8, 2),
        nullable=False,
        default=0,
        doc="Discount percentage.",
    )

    discount_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Discount amount.",
    )

    tax_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Total tax amount.",
    )

    net_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Net amount after discounts and taxes.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional remarks for this Sales Order Item.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether the Sales Order Item is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    sales_order: Mapped["SalesOrder"] = relationship(
        back_populates="items",
    )

    quotation_item: Mapped["SalesQuotationItem"] = relationship()

    product: Mapped["Product"] = relationship(
        back_populates="sales_order_items",
    )

    product_variant: Mapped["ProductVariant"] = relationship(
        back_populates="sales_order_items",
    )

    warehouse: Mapped["Warehouse"] = relationship(
        back_populates="sales_order_items",
    )

    uom: Mapped["UOM"] = relationship(
        back_populates="sales_order_items",
    )