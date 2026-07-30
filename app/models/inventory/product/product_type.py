from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
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


class ProductType(BaseModel):
    """
    Represents the business classification of a Product.

    Purpose:
        Product Types define the operational behavior of products within
        the ERP. Rather than identifying what a product is, a Product Type
        determines how the ERP should process that product during
        purchasing, inventory, manufacturing, sales, accounting, and
        logistics.

        Every Product belongs to exactly one Product Type.

        Product Types drive business rules such as:

            • Whether inventory is tracked.
            • Whether manufacturing is allowed.
            • Whether batch tracking is supported.
            • Whether serial numbers are required.
            • Whether purchasing is allowed.
            • Whether selling is allowed.
            • Whether valuation affects accounting.

    Common Product Types:

        • Physical Product
        • Service
        • Raw Material
        • Semi Finished Good
        • Finished Good
        • Consumable
        • Spare Part
        • Asset
        • Digital Product

    Examples:

        Physical Product
            Dell Laptop
            Office Chair

        Service
            Installation
            Consulting
            Website Development

        Raw Material
            Steel Rod
            Cotton Fabric

        Semi Finished Good
            Bicycle Frame
            Wooden Panel

        Finished Good
            Dining Table
            Desktop Computer

        Consumable
            Printer Ink
            Lubricant
            Cleaning Liquid

        Asset
            CNC Machine
            Generator

        Digital Product
            Software License
            Antivirus Subscription

    Workflow:

                    Product Type
                          │
                          ▼
                       Product
                          │
          ┌───────────────┼────────────────┐
          ▼               ▼                ▼
      Purchase       Inventory       Manufacturing
          │               │                │
          ▼               ▼                ▼
       Sales         Stock Ledger     Accounting

    ERP Behaviour Examples:

        Service
            ✓ Can Sell
            ✓ Can Purchase
            ✗ No Inventory
            ✗ No Warehouse
            ✗ No Batch
            ✗ No Serial

        Finished Good
            ✓ Purchase
            ✓ Sell
            ✓ Inventory
            ✓ Warehouse
            ✓ Stock Valuation

        Raw Material
            ✓ Purchase
            ✓ Inventory
            ✓ Manufacturing Consumption

        Digital Product
            ✓ Sell
            ✗ Inventory
            ✗ Warehouse

    Benefits:

        • Centralizes ERP business rules.
        • Eliminates hard-coded product logic.
        • Simplifies future expansion.
        • Supports configurable ERP workflows.
        • Enables different inventory behaviors.
        • Improves reporting and analytics.
        • Supports Manufacturing, POS, CRM, Sales,
          Purchase, Accounting, and Inventory modules.

    Relationships:

                    ProductType
                          │
                          ▼
                       Products

    Notes:

        • Product Types do not store inventory.
        • Product Types do not store prices.
        • Product Types do not store taxes.
        • Product Types define ERP behavior only.
        • New product types can be added without
          modifying existing product records.

    Example Seed Data:

        PRODUCT
        SERVICE
        RAW_MATERIAL
        SEMI_FINISHED
        FINISHED_GOOD
        CONSUMABLE
        SPARE_PART
        ASSET
        DIGITAL_PRODUCT

    This model acts as the behavioral master for the
    Inventory, Purchase, Sales, Manufacturing,
    Accounting, POS, CRM, and Reporting modules.
    """

    __tablename__ = "product_types"

    code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
        doc="Unique code identifying the product type.",
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
        index=True,
        doc="Display name of the product type.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Detailed description of the product type.",
    )

    is_inventory_item: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether inventory quantities are tracked.",
    )

    is_purchaseable: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether this product type can be purchased.",
    )

    is_sellable: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether this product type can be sold.",
    )

    is_manufacturable: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether products of this type can be manufactured.",
    )

    supports_batch_tracking: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether batch tracking is supported.",
    )

    supports_serial_tracking: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether serial number tracking is supported.",
    )

    affects_inventory_valuation: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Determines whether inventory valuation is affected.",
    )

    is_system: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether this is a predefined system product type.",
    )

    display_order: Mapped[int] = mapped_column(
        nullable=False,
        default=1,
        doc="Display sequence when listing product types.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether the product type is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    products: Mapped[list["Product"]] = relationship(
        back_populates="product_type",
    )