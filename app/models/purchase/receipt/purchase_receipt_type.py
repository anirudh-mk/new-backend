from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.company.company import Company
    from app.models.purchase.receipt.purchase_receipt import PurchaseReceipt


class PurchaseReceiptType(BaseModel):
    """
    Defines the various types of Purchase Receipts.

    Purpose:
        Purchase Receipt Types classify how goods are received from
        suppliers. Instead of hardcoding receipt categories, this
        configurable master allows organizations to define receipt
        types according to their procurement and inventory processes.

        Purchase Receipt Types help inventory operations, warehouse
        management, quality control, reporting, and auditing.

    Common Types:

        • Normal Receipt
            Complete receipt against a Purchase Order.

        • Partial Receipt
            Only part of the ordered quantity is received.

        • Excess Receipt
            Quantity received exceeds the ordered quantity.

        • Replacement Receipt
            Supplier sends replacement goods.

        • Sample Receipt
            Items received for evaluation or testing.

        • Consignment Receipt
            Goods received on consignment.

        • Import Receipt
            Goods received from international suppliers.

    Example:

        Purchase Order
              │
              ▼
        Purchase Receipt
              │
        Receipt Type = Partial Receipt

    Benefits:
        • Standardizes receipt processing.
        • Supports warehouse operations.
        • Enables inventory analysis.
        • Supports quality inspection workflows.
        • Configurable without code changes.
        • Improves procurement reporting.

    Relationships:

        PurchaseReceiptType
                │
                └── PurchaseReceipt
    """

    __tablename__ = "purchase_receipt_types"

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "code",
            name="uq_purchase_receipt_type_company_code",
        ),
    )

    company_id: Mapped[int | None] = mapped_column(
        ForeignKey("companies.id"),
        nullable=True,
        index=True,
        doc="Company owning this receipt type. NULL indicates a global receipt type.",
    )

    code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        doc="Unique purchase receipt type code.",
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="Purchase receipt type name.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Detailed description of the purchase receipt type.",
    )

    updates_inventory: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether receipts of this type update inventory quantities.",
    )

    requires_quality_inspection: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether received goods require quality inspection before being accepted.",
    )

    is_system: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether this is a predefined system receipt type.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether this receipt type is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    company: Mapped["Company"] = relationship()

    purchase_receipts: Mapped[list["PurchaseReceipt"]] = relationship(
        back_populates="receipt_type",
    )
