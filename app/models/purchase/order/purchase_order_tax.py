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
    from app.models.accounting.tax_type import TaxType
    from app.models.purchase.order.purchase_order import PurchaseOrder


class PurchaseOrderTax(BaseModel):
    """
    Represents a tax applied to a Purchase Order.

    Purpose:
        Purchase Order Tax stores document-level tax details calculated
        for a Purchase Order. Multiple tax records may exist for a
        single Purchase Order, allowing support for GST, VAT, customs,
        and other tax structures.

        These taxes represent the estimated tax liability during the
        procurement process and may later be copied or recalculated on
        the corresponding Purchase Invoice.

    Examples:

        • CGST
        • SGST
        • IGST
        • VAT
        • TCS
        • Customs Duty

    Benefits:

        • Supports multiple taxes
        • Easy tax reporting
        • Procurement cost estimation
        • Accounting integration
        • Audit compliance

    Relationships:

        PurchaseOrder
                │
                └── PurchaseOrderTax

        TaxType
                │
                └── PurchaseOrderTax
    """

    __tablename__ = "purchase_order_taxes"

    purchase_order_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_orders.id"),
        nullable=False,
        index=True,
        doc="Reference to the Purchase Order.",
    )

    tax_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("tax_types.id"),
        nullable=False,
        index=True,
        doc="Type of tax.",
    )

    tax_percentage: Mapped[float] = mapped_column(
        Numeric(8, 2),
        nullable=False,
        default=0,
        doc="Tax percentage.",
    )

    taxable_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Amount on which tax is calculated.",
    )

    tax_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Calculated tax amount.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional remarks.",
    )

    line_no: Mapped[int] = mapped_column(
        nullable=False,
        doc="Line number within the Purchase Order tax section.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    purchase_order: Mapped["PurchaseOrder"] = relationship(
        back_populates="taxes",
    )

    tax_type: Mapped["TaxType"] = relationship()