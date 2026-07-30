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


class ProductBrand(BaseModel):
    """
    Represents the manufacturer or commercial brand of a Product.

    Purpose:
        Product Brands identify the manufacturer, trademark, or commercial
        identity associated with a product.

        Brands allow businesses to organize products by manufacturer,
        perform brand-wise reporting, manage supplier relationships,
        implement pricing strategies, and improve customer search
        experiences.

        A single Brand may be associated with multiple Products, while
        each Product typically belongs to one Brand.

    Examples:

        Electronics
            • Apple
            • Samsung
            • Dell
            • HP
            • Lenovo

        Clothing
            • Nike
            • Adidas
            • Puma

        Furniture
            • IKEA
            • Herman Miller

        Automotive
            • Toyota
            • Honda
            • Bosch

    Workflow:

                    Product Brand
                          │
                          ▼
                       Products
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
     Purchase          Inventory          Sales
        │                 │                 │
        ▼                 ▼                 ▼
    Reporting      Business Analytics    E-Commerce

    Benefits:

        • Organizes products by manufacturer.
        • Enables brand-wise reporting.
        • Simplifies product searching.
        • Supports brand-specific pricing.
        • Supports supplier management.
        • Enables warranty tracking.
        • Improves customer browsing.
        • Supports promotional campaigns.
        • Enhances business analytics.

    Relationships:

                ProductBrand
                      │
                      ▼
                   Products

    Notes:

        • Brands do NOT store inventory.
        • Brands do NOT store pricing.
        • Brands do NOT store taxes.
        • Brands are reusable across multiple products.
        • A Product may optionally belong to a Brand.

    This model is referenced throughout Inventory,
    Purchase, Sales, CRM, POS, Reporting,
    E-Commerce, and Business Intelligence modules.
    """

    __tablename__ = "product_brands"

    code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
        index=True,
        doc="Unique product brand code.",
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
        index=True,
        doc="Display name of the product brand.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Detailed description of the product brand.",
    )

    website: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        doc="Official website of the brand.",
    )

    contact_email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        doc="Official contact email of the brand.",
    )

    contact_phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
        doc="Official contact phone number of the brand.",
    )

    country_of_origin: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        doc="Country where the brand originated.",
    )

    logo_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        doc="URL of the brand logo.",
    )

    display_order: Mapped[int] = mapped_column(
        nullable=False,
        default=1,
        doc="Display sequence when listing brands.",
    )

    is_system: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether this is a predefined system brand.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether the brand is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    products: Mapped[list["Product"]] = relationship(
        back_populates="brand",
    )