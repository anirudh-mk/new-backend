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
    from app.models.accounting.charge_type import ChargeType
    from app.models.purchase.order.purchase_order import PurchaseOrder


class PurchaseOrderCharge(BaseModel):
    """
    Represents an additional charge applied to a Purchase Order.

    Purpose:
        Purchase Order Charge stores document-level charges that are
        expected to be incurred during procurement. These charges are
        independent of individual purchase order items and apply to the
        overall Purchase Order.

        The charges may later be copied or adjusted when creating the
        corresponding Purchase Invoice.

    Examples:

        • Freight Charge
        • Transportation
        • Insurance
        • Customs Duty
        • Handling Charge
        • Loading / Unloading
        • Packaging
        • Documentation Fee

    Benefits:

        • Supports multiple additional charges
        • Separate from item pricing
        • Supports tax calculation
        • Can be carried forward to Purchase Invoice
        • Complete procurement audit trail

    Relationships:

        PurchaseOrder
                │
                └── PurchaseOrderCharge

        ChargeType
                │
                └── PurchaseOrderCharge
    """

    __tablename__ = "purchase_order_charges"

    purchase_order_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_orders.id"),
        nullable=False,
        index=True,
        doc="Reference to the Purchase Order.",
    )

    charge_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("charge_types.id"),
        nullable=False,
        index=True,
        doc="Type of additional charge.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional description of the charge.",
    )

    amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Charge amount before tax.",
    )

    tax_percentage: Mapped[float] = mapped_column(
        Numeric(8, 2),
        nullable=False,
        default=0,
        doc="Tax percentage applied to the charge.",
    )

    tax_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Tax amount for the charge.",
    )

    line_total: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Total charge amount including tax.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional remarks.",
    )

    line_no: Mapped[int] = mapped_column(
        nullable=False,
        doc="Line number within the Purchase Order.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    purchase_order: Mapped["PurchaseOrder"] = relationship(
        back_populates="charges",
    )

    charge_type: Mapped["ChargeType"] = relationship()