from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Date,
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.inventory.product.product import Product
    from app.models.inventory.product.product_variant import ProductVariant
    from app.models.inventory.uom.uom import UOM
    from app.models.purchase.requisition.purchase_requisition import PurchaseRequisition


class PurchaseRequisitionItem(BaseModel):
    """
    Represents a single line item in a Purchase Requisition.

    Purpose:
        A Purchase Requisition Item specifies an individual product or
        service requested by a department or employee. Each requisition
        may contain one or more line items, each with its own quantity,
        unit of measure, and required delivery date.

        The approved quantity may differ from the requested quantity
        after review by the purchasing department.

    Workflow:

        Purchase Requisition
                │
                ├── Item 1
                ├── Item 2
                ├── Item 3
                └── Item N

                │
                ▼

        Request For Quotation

    Benefits:
        • Supports multiple products per requisition.
        • Maintains requested and approved quantities.
        • Tracks required delivery dates.
        • Enables procurement planning.
        • Supports complete audit history.

    Relationships:

        PurchaseRequisition
                │
                └── PurchaseRequisitionItem

        Product
                │
                └── PurchaseRequisitionItem

        ProductVariant
                │
                └── PurchaseRequisitionItem

        UOM
                │
                └── PurchaseRequisitionItem
    """

    __tablename__ = "purchase_requisition_items"

    purchase_requisition_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_requisitions.id"),
        nullable=False,
        index=True,
        doc="Reference to the Purchase Requisition.",
    )

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
        doc="Requested product.",
    )

    variant_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("product_variants.id"),
        nullable=True,
        index=True,
        doc="Product variant if applicable.",
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        doc="Additional description for the requested item.",
    )

    uom_id: Mapped[UUID] = mapped_column(
        ForeignKey("uoms.id"),
        nullable=False,
        index=True,
        doc="Unit of Measure for the requested quantity.",
    )

    quantity: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        doc="Requested quantity.",
    )

    approved_quantity: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        default=0,
        doc="Approved quantity after requisition review.",
    )

    required_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        doc="Required delivery date for the item.",
    )

    remarks: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        doc="Additional remarks for this requisition item.",
    )

    line_no: Mapped[int] = mapped_column(
        nullable=False,
        doc="Line number within the Purchase Requisition.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    purchase_requisition: Mapped["PurchaseRequisition"] = relationship(
        back_populates="items",
    )

    product: Mapped["Product"] = relationship()

    variant: Mapped["ProductVariant"] = relationship()

    uom: Mapped["UOM"] = relationship()