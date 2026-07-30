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


class ProductGroup(BaseModel):
    """
    Represents a business grouping of Products within the ERP.

    Purpose:
        Product Groups provide an additional level of business organization
        independent of Product Categories.

        While Product Categories describe what a product is, Product Groups
        define how products are managed from a commercial and operational
        perspective.

        A Product Group may contain products from multiple categories,
        allowing businesses to perform reporting, pricing, promotions,
        procurement, and sales analysis across related products.

    Difference Between Category and Group:

        Category
            Defines the product classification.

            Example:
                Electronics
                Furniture
                Services

        Product Group
            Defines a business or commercial grouping.

            Example:
                Office Equipment
                Premium Products
                Promotional Items
                Seasonal Products

    Examples:

        Office Equipment
            • Dell Laptop
            • HP Printer
            • Office Chair

        Premium Products
            • MacBook Pro
            • iPhone Pro
            • Samsung Fold

        Seasonal Products
            • Christmas Tree
            • Decorative Lights
            • Gift Box

        Fast Moving Items
            • Water Bottle
            • Soft Drinks
            • Snacks

    Workflow:

                    Product Group
                          │
                          ▼
                      Products
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
     Purchase          Inventory          Sales
        │                 │                 │
        ▼                 ▼                 ▼
     Reports         Dashboards      Business Analytics

    Benefits:

        • Business-oriented product organization.
        • Cross-category reporting.
        • Simplifies pricing strategies.
        • Supports promotional campaigns.
        • Supports commission calculations.
        • Enables group-wise sales analysis.
        • Enables procurement analysis.
        • Improves dashboard reporting.
        • Simplifies business intelligence.

    Relationships:

                ProductGroup
                      │
                      ▼
                  Products

    Notes:

        • Product Groups are NOT hierarchical.
        • Product Groups do NOT store inventory.
        • Product Groups do NOT store pricing.
        • Product Groups do NOT store taxes.
        • A Product Group is primarily used for reporting,
          analytics, pricing policies, and commercial operations.

    This model is referenced throughout Inventory,
    Purchase, Sales, CRM, POS, Reporting,
    Marketing, and Business Intelligence modules.
    """

    __tablename__ = "product_groups"

    code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
        index=True,
        doc="Unique product group code.",
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
        index=True,
        doc="Display name of the product group.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Detailed description of the product group.",
    )

    display_order: Mapped[int] = mapped_column(
        nullable=False,
        default=1,
        doc="Display sequence for listing product groups.",
    )

    is_system: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether this is a predefined system group.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether the product group is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    products: Mapped[list["Product"]] = relationship(
        back_populates="group",
    )