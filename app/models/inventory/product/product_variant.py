from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
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
    from app.models.inventory.stock.stock import Stock
    from app.models.inventory.product.product_variant_attribute import ProductVariantAttribute
    from app.models.inventory.product.product_price import ProductPrice
    from app.models.inventory.product.product_image import ProductImage

    from app.models.purchase.order.purchase_order_item import PurchaseOrderItem
    from app.models.sales.order.sales_order_item import SalesOrderItem


class ProductVariant(BaseModel):
    """
    Represents a specific purchasable and sellable variation of a Product.

    Purpose:
        A Product Variant represents an individual Stock Keeping Unit (SKU)
        created from a unique combination of Product Attributes.

        While the Product model stores common master information,
        Product Variants represent the actual items managed by
        Inventory, Purchase, Sales, Manufacturing, POS,
        and Warehouse operations.

        Every inventory movement, purchase, sales transaction,
        barcode, serial number, and stock balance is generally
        maintained against a Product Variant.

    Examples:

        Product
            T-Shirt

                Variant
                    Red / Small

                Variant
                    Red / Medium

                Variant
                    Blue / Large

        Product
            iPhone 16

                Variant
                    Black / 128 GB

                Variant
                    Black / 256 GB

                Variant
                    Blue / 128 GB

    Workflow:

                    Product
                       │
            ┌──────────┼──────────┐
            ▼          ▼          ▼
       Variant     Variant     Variant
            │          │          │
            ▼          ▼          ▼
      Purchase    Inventory     Sales
            │          │          │
            ▼          ▼          ▼
      Stock Ledger  Warehouse  Invoice

    Benefits:

        • Supports unlimited product variations.
        • Independent SKU for every variation.
        • Independent barcode.
        • Independent pricing.
        • Independent inventory.
        • Supports batch tracking.
        • Supports serial tracking.
        • Supports warehouse management.
        • Supports manufacturing.
        • Complete inventory traceability.

    Relationships:

                    Product
                       │
                       ▼
                 ProductVariant
                       │
          ┌────────────┼─────────────┐
          ▼            ▼             ▼
     Variant      ProductPrice     Stock
    Attributes
          │
          ▼
      Purchase
      Sales

    Examples:

        Product
            Laptop

        Variant
            i5 / 8GB / 256GB

        Variant
            i7 / 16GB / 512GB

        Product
            Shoes

        Variant
            Black / Size 42

        Variant
            White / Size 43

    Notes:

        • Inventory is maintained at Variant level.
        • Prices may differ between variants.
        • Every Variant should have its own SKU.
        • Every Variant may have its own barcode.
        • Variants inherit common information from Product.

    This model is referenced throughout Inventory,
    Purchase, Sales, Manufacturing,
    Warehouse, POS, CRM, and Reporting modules.
    """

    __tablename__ = "product_variants"

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
        doc="Reference to the parent Product.",
    )

    sku: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
        doc="Unique Stock Keeping Unit for this variant.",
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        doc="Display name of the product variant.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional description for this variant.",
    )

    barcode: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        unique=True,
        index=True,
        doc="Barcode assigned to this product variant.",
    )

    weight: Mapped[float | None] = mapped_column(
        Numeric(18, 4),
        nullable=True,
        doc="Weight of one unit of this variant.",
    )

    volume: Mapped[float | None] = mapped_column(
        Numeric(18, 4),
        nullable=True,
        doc="Volume occupied by one unit.",
    )

    sort_order: Mapped[int] = mapped_column(
        nullable=False,
        default=1,
        doc="Display sequence of this variant.",
    )

    is_default: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether this is the default variant.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether this variant is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    product: Mapped["Product"] = relationship(
        back_populates="variants",
    )

    attributes: Mapped[list["ProductVariantAttribute"]] = relationship(
        back_populates="variant",
        cascade="all, delete-orphan",
    )

    prices: Mapped[list["ProductPrice"]] = relationship(
        back_populates="variant",
        cascade="all, delete-orphan",
    )

    images: Mapped[list["ProductImage"]] = relationship(
        back_populates="variant",
        cascade="all, delete-orphan",
    )

    stock: Mapped[list["Stock"]] = relationship(
        back_populates="variant",
    )

    purchase_order_items: Mapped[list["PurchaseOrderItem"]] = relationship()

    sales_order_items: Mapped[list["SalesOrderItem"]] = relationship()