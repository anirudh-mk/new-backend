from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
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
    from app.models.inventory.uom.uom import UOM
    from app.models.sales.quotation.sales_quotation import SalesQuotation


class SalesQuotationItem(BaseModel):
    """
    Represents an individual Product line within a Sales Quotation.

    Purpose:
        Sales Quotation Item stores the products or services
        offered to a customer as part of a Sales Quotation.

        Every quotation consists of one or more quotation items.

        Each item maintains product information,
        quantity,
        unit price,
        discount,
        tax amount,
        and line total.

        Item-level taxes, batches,
        serial numbers,
        and additional charges
        should be maintained in dedicated tables.

    Examples:

        Quotation

            QT-00045

        Item 1

            Laptop
            Qty : 5
            Rate : ₹52,000

        Item 2

            Mouse
            Qty : 5
            Rate : ₹850

    Workflow:

              Sales Quotation
                     │
                     ▼
          Sales Quotation Item
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
     Product      Tax Lines    Discounts
                     │
                     ▼
              Sales Order Item

    Benefits:

        • Supports unlimited quotation lines.
        • Product variant support.
        • Service item support.
        • Independent pricing.
        • Independent discounts.
        • Item-level tax calculation.
        • Partial order conversion.
        • Margin calculation.
        • Profitability analysis.
        • Inventory integration.

    Relationships:

               SalesQuotation
                     │
                     ▼
            SalesQuotationItem
             ┌──────┼────────┐
             ▼      ▼        ▼
         Product Variant    UOM

    Example:

        Product

            Dell Latitude 5450

        Variant

            16GB / 512GB

        Quantity

            10

        Unit Price

            ₹58,000

        Discount

            ₹2,000

        Net Amount

            ₹5,60,000

    Notes:

        • One quotation contains many items.
        • Items may be products or services.
        • Taxes are stored separately.
        • Multiple discounts may be supported.
        • Item may later become a Sales Order Item.
        • Supports product variants.
        • Supports future pricing updates.
        • Historical quotation items are immutable.

    This model is referenced throughout
    Sales,
    Inventory,
    Pricing,
    Taxation,
    Sales Order,
    Reporting,
    Analytics,
    and CRM modules.
    """

    __tablename__ = "sales_quotation_items"

    quotation_id: Mapped[UUID] = mapped_column(
        ForeignKey("sales_quotations.id"),
        nullable=False,
        index=True,
        doc="Reference to the Sales Quotation.",
    )

    line_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        doc="Sequential line number.",
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

    uom_id: Mapped[UUID] = mapped_column(
        ForeignKey("uoms.id"),
        nullable=False,
        index=True,
        doc="Reference to the Unit of Measure.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Product description printed on the quotation.",
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(18, 3),
        nullable=False,
        default=1,
        doc="Quoted quantity.",
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
        doc="Total tax amount for the line.",
    )

    net_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Net amount after discounts and taxes.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional remarks for the quotation item.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether this quotation item is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    quotation: Mapped["SalesQuotation"] = relationship(
        back_populates="items",
    )

    product: Mapped["Product"] = relationship(
        back_populates="sales_quotation_items",
    )

    product_variant: Mapped["ProductVariant"] = relationship(
        back_populates="sales_quotation_items",
    )

    uom: Mapped["UOM"] = relationship(
        back_populates="sales_quotation_items",
    )