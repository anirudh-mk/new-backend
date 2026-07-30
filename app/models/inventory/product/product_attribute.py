from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
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
    from app.models.inventory.product.product_attribute_value import ProductAttributeValue


class ProductAttribute(BaseModel):
    """
    Represents a configurable characteristic of a Product.

    Purpose:
        Product Attributes define the characteristics that distinguish one
        Product Variant from another.

        Attributes themselves do not store any values. Instead, they define
        the attribute type, while the possible values are maintained in the
        ProductAttributeValue master.

        Examples of Product Attributes include Color, Size, Storage,
        Material, Capacity, Voltage, RAM, and Length.

        During Product Variant creation, one value from each applicable
        attribute is selected to form a unique SKU.

    Examples:

        Clothing

            Attribute
                Color

            Values
                Red
                Blue
                Black

            Attribute
                Size

            Values
                Small
                Medium
                Large

        Laptop

            Attribute
                RAM

            Values
                8 GB
                16 GB
                32 GB

            Attribute
                Storage

            Values
                256 GB
                512 GB
                1 TB

    Workflow:

                    Product
                       │
                       ▼
              Product Attribute
                       │
                       ▼
          Product Attribute Values
                       │
                       ▼
                Product Variant
                       │
                       ▼
            Purchase / Inventory / Sales

    Benefits:

        • Supports unlimited product configurations.
        • Eliminates duplicated attribute definitions.
        • Enables automatic SKU generation.
        • Supports configurable products.
        • Improves product searching.
        • Enables attribute-based filtering.
        • Simplifies e-commerce product filters.
        • Supports inventory at variant level.
        • Improves reporting and analytics.

    Relationships:

                    Product
                       │
                       ▼
               ProductAttribute
                       │
                       ▼
            ProductAttributeValue
                       │
                       ▼
               ProductVariantAttribute
                       │
                       ▼
                 ProductVariant

    Example:

        Product
            T-Shirt

        Attributes

            Color
                Red
                Blue
                Black

            Size
                S
                M
                L
                XL

        Generated Variants

            Red / S
            Red / M
            Red / L
            Blue / S
            Blue / M
            ...

    Notes:

        • Attributes do not contain inventory.
        • Attributes do not contain pricing.
        • Attributes do not contain stock.
        • Values are stored separately.
        • Multiple Products may share the same Attribute.
        • Products may use zero or many Attributes.

    This model is referenced throughout Inventory,
    Purchase, Sales, Manufacturing,
    POS, CRM, Reporting, and E-Commerce modules.
    """

    __tablename__ = "product_attributes"

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
        doc="Reference to the Product that owns this attribute.",
    )

    code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="Unique attribute code within the product.",
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        doc="Display name of the product attribute.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Detailed description of the attribute.",
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
        doc="Display order when presenting attributes.",
    )

    is_required: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether the attribute is mandatory for variant generation.",
    )

    allow_custom_value: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Allows users to enter values that are not predefined.",
    )

    is_variant_attribute: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Determines whether this attribute participates in variant generation.",
    )

    is_filterable: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Determines whether this attribute can be used in search and filtering.",
    )

    display_on_documents: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Determines whether the attribute appears on business documents.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether the attribute is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    product: Mapped["Product"] = relationship(
        back_populates="attributes",
    )

    values: Mapped[list["ProductAttributeValue"]] = relationship(
        back_populates="attribute",
        cascade="all, delete-orphan",
    )