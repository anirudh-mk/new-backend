from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    Date,
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
    from app.models.sales.master.sales_price_list import SalesPriceList


class CustomerPrice(BaseModel):
    """
    Represents a customer-specific selling price for a Product or Product Variant.

    Purpose:
        Customer Price stores negotiated selling prices for individual
        customers.

        While Sales Price Lists define standard pricing strategies,
        Customer Price allows overriding those prices for specific
        customers.

        This enables enterprises to support contract pricing,
        negotiated pricing, dealer pricing, distributor pricing,
        corporate pricing, government pricing, promotional pricing,
        and customer-exclusive discounts.

        During Sales Quotation, Sales Order, or Sales Invoice creation,
        the pricing engine first checks Customer Price before falling
        back to the assigned Sales Price List.

    Examples:

        Customer

            ABC Supermarket

        Product

            Rice 25 KG

        Standard Price

            ₹1,450

        Customer Price

            ₹1,390

        -------------------------------------

        Customer

            XYZ Hospital

        Product

            Surgical Gloves

        Standard Price

            ₹320

        Contract Price

            ₹285

    Workflow:

                     Company
                        │
                        ▼
                  Sales Price List
                        │
                        ▼
                  Customer Price
                        │
            ┌───────────┴───────────┐
            ▼                       ▼
         Customer               Product
                                        │
                                        ▼
                              Product Variant
                                        │
                                        ▼
                              Sales Quotation
                                        │
                                        ▼
                                Sales Order
                                        │
                                        ▼
                               Sales Invoice

    Benefits:

        • Supports negotiated pricing.
        • Supports contract pricing.
        • Supports customer-specific discounts.
        • Eliminates manual price changes.
        • Supports dealer pricing.
        • Supports distributor pricing.
        • Supports promotional pricing.
        • Supports future pricing.
        • Supports variant-wise pricing.
        • Enables pricing automation.

    Relationships:

                     Company
                        │
                        ▼
                  Customer Price
                ┌──────┼──────┐
                ▼      ▼      ▼
          SalesPriceList Customer Product
                               │
                               ▼
                        Product Variant

    Example:

        Customer

            ABC Traders

        Product

            Dell Laptop

        Price List

            Dealer Price

        Selling Price

            ₹52,500

        Valid

            01-Jan-2026
                    ↓
            31-Dec-2026

    Notes:

        • One Customer may have multiple Product Prices.
        • One Product may have multiple Customer Prices.
        • Variant pricing overrides Product pricing.
        • Price Lists act as the parent pricing strategy.
        • Expired prices are ignored automatically.
        • Future prices may be maintained.
        • Supports unlimited pricing history.
        • Supports multiple currencies.

    This model is referenced throughout
    CRM,
    Customer Management,
    Pricing Engine,
    Sales,
    Quotation,
    Sales Order,
    Sales Invoice,
    POS,
    E-Commerce,
    and Reporting modules.
    """

    __tablename__ = "customer_prices"

    company_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Reference to the Company.",
    )

    sales_price_list_id: Mapped[UUID] = mapped_column(
        ForeignKey("sales_price_lists.id"),
        nullable=False,
        index=True,
        doc="Reference to the Sales Price List.",
    )

    customer_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Reference to the Customer.",
    )

    product_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Reference to the Product.",
    )

    product_variant_id: Mapped[UUID | None] = mapped_column(
        nullable=True,
        index=True,
        doc="Optional Product Variant. If specified, this price overrides Product pricing.",
    )

    selling_price: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Customer-specific selling price.",
    )

    minimum_quantity: Mapped[float] = mapped_column(
        Numeric(18, 3),
        nullable=False,
        default=1,
        doc="Minimum quantity required for this price.",
    )

    maximum_quantity: Mapped[float | None] = mapped_column(
        Numeric(18, 3),
        nullable=True,
        doc="Maximum quantity applicable for this price.",
    )

    valid_from: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        doc="Price effective start date.",
    )

    valid_to: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        doc="Price expiry date.",
    )

    currency_code: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="INR",
        doc="Currency of the selling price.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Optional remarks about this pricing agreement.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether this Customer Price is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------


    sales_price_list: Mapped["SalesPriceList"] = relationship(
        back_populates="customer_prices",
    )



