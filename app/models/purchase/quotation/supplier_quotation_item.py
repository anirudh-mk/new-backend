from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.inventory.product.product import Product
    from app.models.inventory.product.product_variant import ProductVariant
    from app.models.inventory.uom.uom import UOM

    from app.models.purchase.quotation.supplier_quotation import SupplierQuotation


class SupplierQuotationItem(BaseModel):
    """
    Represents a single quoted item from a supplier.

    Purpose:
        A Supplier Quotation Item records an individual product or
        service quoted by a supplier in response to a Request for
        Quotation (RFQ). Each Supplier Quotation may contain multiple
        items with their own pricing, discounts, taxes, delivery lead
        time, and minimum order quantities.

        These items become the basis for creating Purchase Orders.

    Workflow:

        Request For Quotation
                │
                ▼
        Supplier Quotation
                │
                ▼
        Supplier Quotation Item
                │
                ▼
        Purchase Order Item

    Benefits:
        • Stores supplier pricing.
        • Supports multiple quoted items.
        • Records taxes and discounts.
        • Maintains delivery lead time.
        • Supports supplier price comparison.
        • Complete procurement audit trail.

    Relationships:

        SupplierQuotation
                │
                └── SupplierQuotationItem

        Product
                │
                └── SupplierQuotationItem

        ProductVariant
                │
                └── SupplierQuotationItem

        UOM
                │
                └── SupplierQuotationItem
    """

    __tablename__ = "supplier_quotation_items"

    supplier_quotation_id: Mapped[UUID] = mapped_column(
        ForeignKey("supplier_quotations.id"),
        nullable=False,
        index=True,
        doc="Reference to the Supplier Quotation.",
    )

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
        doc="Quoted product.",
    )

    variant_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("product_variants.id"),
        nullable=True,
        index=True,
        doc="Quoted product variant.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional description of the quoted product.",
    )

    uom_id: Mapped[UUID] = mapped_column(
        ForeignKey("uoms.id"),
        nullable=False,
        index=True,
        doc="Unit of Measure.",
    )

    quoted_quantity: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        doc="Quoted quantity.",
    )

    minimum_order_quantity: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        default=1,
        doc="Minimum quantity required to purchase at the quoted price.",
    )

    unit_price: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        doc="Supplier quoted unit price.",
    )

    discount_percentage: Mapped[float] = mapped_column(
        Numeric(8, 2),
        nullable=False,
        default=0,
        doc="Discount percentage.",
    )

    discount_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Discount amount.",
    )

    tax_percentage: Mapped[float] = mapped_column(
        Numeric(8, 2),
        nullable=False,
        default=0,
        doc="Tax percentage.",
    )

    tax_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Tax amount.",
    )

    line_total: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Net quoted amount for this item.",
    )

    lead_time_days: Mapped[int | None] = mapped_column(
        nullable=True,
        doc="Estimated delivery lead time in days.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional remarks.",
    )

    line_no: Mapped[int] = mapped_column(
        nullable=False,
        doc="Line number within the Supplier Quotation.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    supplier_quotation: Mapped["SupplierQuotation"] = relationship(
        back_populates="items",
    )

    product: Mapped["Product"] = relationship()

    variant: Mapped["ProductVariant"] = relationship()

    uom: Mapped["UOM"] = relationship()