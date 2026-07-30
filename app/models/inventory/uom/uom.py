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
    from app.models.inventory.uom.uom_category import UOMCategory


class UOM(BaseModel):
    """
    Represents a Unit of Measure (UOM) used throughout the ERP.

    Purpose:
        A Unit of Measure defines how quantities of products,
        materials, services, and inventory transactions are measured.

        Every product references one or more Units of Measure
        to ensure consistent quantity calculations across
        Purchasing, Inventory, Sales, Manufacturing,
        Warehouse, POS, and Reporting modules.

        UOMs belong to a UOM Category, allowing automatic
        conversions between compatible measurement units.

    Examples:

        Quantity

            Each
            Pair
            Dozen
            Box
            Carton

        Weight

            Milligram
            Gram
            Kilogram
            Ton

        Length

            Millimeter
            Centimeter
            Meter
            Kilometer

        Volume

            Milliliter
            Liter
            Cubic Meter

        Time

            Minute
            Hour
            Day

    Workflow:

                UOM Category
                      │
                      ▼
                     UOM
                      │
        ┌─────────────┼──────────────┐
        ▼             ▼              ▼
     Product      Purchase       Sales
                      │
                      ▼
                  Inventory
                      │
                      ▼
                Manufacturing

    Benefits:

        • Standardizes quantity measurements.
        • Supports automatic unit conversions.
        • Prevents incompatible measurements.
        • Simplifies inventory calculations.
        • Improves purchasing accuracy.
        • Improves sales consistency.
        • Supports manufacturing BOM calculations.
        • Enables warehouse quantity management.
        • Improves reporting accuracy.

    Relationships:

                UOM Category
                      │
                      ▼
                     UOM
               ┌──────┴──────┐
               ▼             ▼
           Products     Transactions

    Example Conversion:

        Weight Category

            Kilogram (Base)

            Gram
                0.001

            Ton
                1000

        Quantity Category

            Each (Base)

            Box
                12

            Carton
                144

    Notes:

        • Every UOM belongs to one UOM Category.
        • Only UOMs within the same category may be converted.
        • Each category should have exactly one Base UOM.
        • Conversion factors are relative to the Base UOM.
        • UOMs should not be deleted once used in transactions.

    This model is referenced throughout Inventory,
    Purchase, Sales, Manufacturing,
    Warehouse, POS, Accounting,
    and Reporting modules.
    """

    __tablename__ = "uoms"

    uom_category_id: Mapped[UUID] = mapped_column(
        ForeignKey("uom_categories.id"),
        nullable=False,
        index=True,
        doc="Reference to the UOM Category.",
    )

    code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
        index=True,
        doc="Unique Unit of Measure code.",
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
        doc="Display name of the Unit of Measure.",
    )

    symbol: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        doc="Abbreviation or symbol of the Unit of Measure (kg, m, L, pcs).",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Detailed description of the Unit of Measure.",
    )

    conversion_factor: Mapped[float] = mapped_column(
        Numeric(18, 8),
        nullable=False,
        default=1,
        doc="Conversion factor relative to the Base UOM of the category.",
    )

    is_base_uom: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether this is the Base Unit of Measure for its category.",
    )

    decimal_precision: Mapped[int] = mapped_column(
        nullable=False,
        default=2,
        doc="Number of decimal places permitted for quantities.",
    )

    display_order: Mapped[int] = mapped_column(
        nullable=False,
        default=1,
        doc="Display sequence when listing Units of Measure.",
    )

    is_system: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether this is a predefined system UOM.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether this Unit of Measure is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    uom_category: Mapped["UOMCategory"] = relationship(
        back_populates="uoms",
    )

    products: Mapped[list["Product"]] = relationship(
        foreign_keys="Product.base_uom_id",
        back_populates="base_uom",
    )

    purchase_products: Mapped[list["Product"]] = relationship(
        foreign_keys="Product.purchase_uom_id",
        back_populates="purchase_uom",
    )

    sales_products: Mapped[list["Product"]] = relationship(
        foreign_keys="Product.sales_uom_id",
        back_populates="sales_uom",
    )