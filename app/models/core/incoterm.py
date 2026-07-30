from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    pass  # decoupled: from app.models.purchase.order.purchase_order import PurchaseOrder
    from app.models.sales.sales_order import SalesOrder


class Incoterm(AuditModel):
    """
    International Commercial Terms (Incoterms).

    Incoterms are standardized trade terms published by the
    International Chamber of Commerce (ICC) that define the
    responsibilities of buyers and sellers for the delivery
    of goods in domestic and international trade.

    Examples:
        EXW - Ex Works
        FCA - Free Carrier
        FOB - Free On Board
        CFR - Cost and Freight
        CIF - Cost, Insurance and Freight
        CPT - Carriage Paid To
        CIP - Carriage and Insurance Paid To
        DAP - Delivered At Place
        DPU - Delivered at Place Unloaded
        DDP - Delivered Duty Paid

    This table is shared by both Purchase and Sales modules.
    """

    __tablename__ = "incoterms"

    code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False,
        index=True,
        doc="Incoterm code (FOB, CIF, EXW, etc.)",
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="Incoterm full name.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Detailed explanation of the Incoterm.",
    )

    version: Mapped[str] = mapped_column(
        String(10),
        default="2020",
        nullable=False,
        doc="ICC Incoterm version.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------


    sales_orders: Mapped[list["SalesOrder"]] = relationship(
        back_populates="incoterm"
    )

    def __repr__(self) -> str:
        return f"<Incoterm(code='{self.code}', name='{self.name}')>"