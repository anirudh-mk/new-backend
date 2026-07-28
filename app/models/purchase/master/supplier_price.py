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
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.company.company import Company
    from app.models.party.party import Party
    from app.models.inventory.product import Product
    from app.models.inventory.uom import UOM
    from app.models.core.currency import Currency
    from app.models.purchase.supplier_price_type import SupplierPriceType
    from app.models.purchase.master.supplier_price_history import SupplierPriceHistory


class SupplierPrice(AuditModel):
    """
    Represents the agreed purchase price of a product from a supplier.

    Purpose:
        Supplier Price maintains supplier-specific pricing for products.
        It enables the ERP to automatically suggest purchase prices while
        creating Purchase Orders, RFQs, and Supplier Quotations.

        Multiple price records may exist for the same supplier and product,
        allowing historical pricing, future pricing, seasonal pricing,
        contract pricing, and promotional pricing.

        The ERP automatically selects the applicable record based on the
        effective period, quantity, and pricing type.

    ERP Workflow:

        Supplier
            │
            ▼
        Supplier Price
            │
            ▼
        Request For Quotation
            │
            ▼
        Supplier Quotation
            │
            ▼
        Purchase Order
            │
            ▼
        Purchase Receipt
            │
            ▼
        Purchase Invoice

    Business Benefits:
        - Maintains supplier-specific product prices.
        - Supports historical pricing.
        - Supports future price revisions.
        - Supports contract pricing.
        - Supports promotional pricing.
        - Supports quantity-based purchasing.
        - Supports multiple currencies.
        - Stores supplier delivery lead time.
        - Automatically suggests purchase prices.

    Typical Usage:

        Supplier:
            ABC Steel Ltd.

        Product:
            Mild Steel Rod

        Price:
            ₹520.00

        Currency:
            INR

        Minimum Quantity:
            100

        Lead Time:
            14 Days

        Effective:
            01-Jan-2026
            to
            31-Dec-2026

    Relationships:

        Company
            └── SupplierPrice

        Supplier (Party)
            └── SupplierPrice

        Product
            └── SupplierPrice

        Unit Of Measurement
            └── SupplierPrice

        Currency
            └── SupplierPrice

        Supplier Price Type
            └── SupplierPrice

    Example:

        Supplier:
            ABC Suppliers

        Product:
            HP Laptop

        UOM:
            Nos

        Currency:
            INR

        Price:
            ₹48,500

        Price Type:
            Contract

        Lead Time:
            10 Days

        Effective:
            01-Apr-2026

        Expiry:
            31-Mar-2027

        Default:
            Yes
    """

    __tablename__ = "supplier_prices"

    __table_args__ = (
        UniqueConstraint(
            "supplier_id",
            "product_id",
            "uom_id",
            "price_type_id",
            "effective_from",
            name="uq_supplier_product_price",
        ),
    )

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
        doc="Company that owns this supplier price record.",
    )

    supplier_id: Mapped[UUID] = mapped_column(
        ForeignKey("parties.id"),
        nullable=False,
        index=True,
        doc="Supplier offering the product.",
    )

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
        doc="Product for which this price applies.",
    )

    uom_id: Mapped[UUID] = mapped_column(
        ForeignKey("uoms.id"),
        nullable=False,
        index=True,
        doc="Unit of Measure applicable for this price.",
    )

    currency_id: Mapped[UUID] = mapped_column(
        ForeignKey("currencies.id"),
        nullable=False,
        index=True,
        doc="Currency in which the purchase price is maintained.",
    )

    price_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("supplier_price_types.id"),
        nullable=False,
        index=True,
        doc=(
            "Type of supplier pricing such as Standard, Contract, "
            "Promotional, Seasonal or Bulk Pricing."
        ),
    )

    price: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Purchase price offered by the supplier.",
    )
    maximum_quantity: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        default=1,
        doc="Maximum purchase quantity required for this price to apply.",
    )

    minimum_quantity: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        default=1,
        doc="Minimum purchase quantity required for this price to apply.",
    )

    lead_time_days: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
        doc=(
            "Estimated number of days required by the supplier "
            "to deliver the product after confirming the Purchase Order."
        ),
    )

    effective_from: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Date from which this supplier price becomes effective.",
    )

    effective_to: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        doc="Date until which this supplier price remains valid.",
    )

    is_default: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether this is the default supplier price for the product.",
    )

    remarks: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        doc="Additional notes regarding this supplier pricing agreement.",
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    company: Mapped["Company"] = relationship()

    supplier: Mapped["Party"] = relationship()

    product: Mapped["Product"] = relationship()

    uom: Mapped["UOM"] = relationship()

    currency: Mapped["Currency"] = relationship()

    price_type: Mapped["SupplierPriceType"] = relationship()

    history: Mapped[list["SupplierPriceHistory"]] = relationship(
        back_populates="supplier_price",
        cascade="all, delete-orphan",
    )
