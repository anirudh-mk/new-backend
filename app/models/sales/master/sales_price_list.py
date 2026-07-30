from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    Date,
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
    from app.models.company.company import Company
    from app.models.sales.master.customer_price import CustomerPrice


class SalesPriceList(BaseModel):
    """
    Represents a reusable Sales Price List.

    Purpose:
        A Sales Price List defines the pricing strategy used when
        selling products.

        Instead of storing selling prices directly inside Products,
        ERP systems maintain multiple Price Lists to support
        different customers, customer groups, branches,
        currencies, markets, seasons, promotions,
        wholesale pricing, dealer pricing, and retail pricing.

        Every Product may have multiple prices depending on
        which Price List is selected.

    Examples:

        Retail Price List

            Laptop
                ₹55,000

            Mouse
                ₹750

        Wholesale Price List

            Laptop
                ₹51,500

            Mouse
                ₹620

        Dealer Price List

            Laptop
                ₹49,000

            Mouse
                ₹580

        Export Price List

            Laptop
                USD 720

            Mouse
                USD 10

    Workflow:

                    Company
                       │
                       ▼
                Sales Price List
                       │
                       ▼
                 Customer Price
                       │
                       ▼
                   Customer
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

        • Supports unlimited pricing strategies.
        • Supports wholesale and retail pricing.
        • Supports customer-specific pricing.
        • Supports seasonal pricing.
        • Supports promotional pricing.
        • Supports branch-wise pricing.
        • Supports regional pricing.
        • Supports multiple currencies.
        • Eliminates duplicate price maintenance.
        • Simplifies future price updates.

    Relationships:

                    Company
                       │
                       ▼
                SalesPriceList
                       │
                       ▼
                 CustomerPrice
                       │
                       ▼
                    Product

    Example:

        Code

            RETAIL

        Name

            Retail Price List

        Currency

            INR

        Priority

            1

        Validity

            01-Jan-2026
                    ↓
            31-Dec-2026

    Notes:

        • One Company may maintain multiple Price Lists.
        • Price Lists may overlap.
        • Higher priority lists are selected first.
        • A Price List itself does not store Product prices.
        • Product prices are maintained separately.
        • Price Lists may be assigned to Customers.
        • Price Lists may be assigned to Customer Groups.
        • Promotional Price Lists may have expiry dates.
        • Supports future price planning.

    This model is referenced throughout
    CRM,
    Sales,
    Quotation,
    Sales Order,
    Sales Invoice,
    POS,
    E-Commerce,
    Customer Pricing,
    Pricing Engine,
    and Reporting modules.
    """

    __tablename__ = "sales_price_lists"

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
        doc="Reference to the Company that owns this Price List.",
    )

    code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
        doc="Unique Price List code.",
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
        doc="Display name of the Price List.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Optional description explaining the purpose of this Price List.",
    )

    currency_code: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="INR",
        doc="Currency used by this Price List.",
    )

    priority: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
        doc="Priority used when multiple Price Lists are applicable.",
    )

    price_factor: Mapped[float] = mapped_column(
        Numeric(10, 4),
        nullable=False,
        default=1.0000,
        doc="Multiplier applied by the pricing engine if automatic pricing is enabled.",
    )

    valid_from: Mapped[Date | None] = mapped_column(
        Date,
        nullable=True,
        doc="Date from which this Price List becomes effective.",
    )

    valid_to: Mapped[Date | None] = mapped_column(
        Date,
        nullable=True,
        doc="Date until which this Price List remains valid.",
    )

    is_default: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether this is the default Price List.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether this Price List is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    company: Mapped["Company"] = relationship(
        back_populates="sales_price_lists",
    )

    customer_prices: Mapped[list["CustomerPrice"]] = relationship(
        back_populates="sales_price_list",
        cascade="all, delete-orphan",
    )