from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    Numeric,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.inventory.product.product import Product
    from app.models.inventory.product.product_variant import ProductVariant
    from app.models.purchase.receipt.purchase_receipt_item import PurchaseReceiptItem
    from app.models.purchase.inspection.purchase_inspection import PurchaseInspection
    from app.models.support.inspection_result import InspectionResult


class PurchaseInspectionItem(BaseModel):
    """
    Represents the inspection result of a received purchase item.

    Purpose:
        Purchase Inspection Item stores the inspection outcome for an
        individual Purchase Receipt Item. Each inspection item records
        accepted and rejected quantities, inspection result, and any
        quality-related remarks.

        These records determine whether goods are accepted into
        inventory or returned to the supplier.

    Workflow:

        Purchase Receipt Item
                │
                ▼
        Purchase Inspection Item
          │               │
          ▼               ▼
      Accepted        Rejected
          │               │
          ▼               ▼
      Inventory      Purchase Return

    Benefits:

        • Line-level quality inspection
        • Accepted and rejected quantity tracking
        • Supplier quality analysis
        • Purchase return integration
        • Inventory validation
        • Complete audit trail

    Relationships:

        PurchaseInspection
                │
                └── PurchaseInspectionItem

        PurchaseReceiptItem
                │
                └── PurchaseInspectionItem

        Product
                │
                └── PurchaseInspectionItem

        ProductVariant
                │
                └── PurchaseInspectionItem

        InspectionResult
                │
                └── PurchaseInspectionItem
    """

    __tablename__ = "purchase_inspection_items"

    purchase_inspection_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_inspections.id"),
        nullable=False,
        index=True,
        doc="Reference to the Purchase Inspection.",
    )

    purchase_receipt_item_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_receipt_items.id"),
        nullable=False,
        index=True,
        doc="Reference to the Purchase Receipt Item.",
    )

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
        doc="Inspected product.",
    )

    variant_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("product_variants.id"),
        nullable=True,
        index=True,
        doc="Inspected product variant.",
    )

    accepted_quantity: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        default=0,
        doc="Quantity accepted after inspection.",
    )

    rejected_quantity: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        default=0,
        doc="Quantity rejected after inspection.",
    )

    inspection_result_id: Mapped[UUID] = mapped_column(
        ForeignKey("inspection_results.id"),
        nullable=False,
        index=True,
        doc="Inspection result.",
    )

    reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Reason for rejection or observation.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional inspection remarks.",
    )

    line_no: Mapped[int] = mapped_column(
        nullable=False,
        doc="Line number within the Purchase Inspection.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    purchase_inspection: Mapped["PurchaseInspection"] = relationship(
        back_populates="items",
    )

    purchase_receipt_item: Mapped["PurchaseReceiptItem"] = relationship()

    product: Mapped["Product"] = relationship()

    variant: Mapped["ProductVariant"] = relationship()

    inspection_result: Mapped["InspectionResult"] = relationship()

    inspection_details: Mapped[list["PurchaseInspectionDetail"]] = relationship(
        back_populates="purchase_inspection_item",
        cascade="all, delete-orphan",
    )