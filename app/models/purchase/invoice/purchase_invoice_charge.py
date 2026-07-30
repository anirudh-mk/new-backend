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
    pass  # decoupled: from app.models.accounting.charge_type import ChargeType
    from app.models.purchase.invoice.purchase_invoice import PurchaseInvoice


class PurchaseInvoiceCharge(BaseModel):
    """
    Represents an additional charge applied to a Purchase Invoice.
    """

    __tablename__ = "purchase_invoice_charges"

    purchase_invoice_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_invoices.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Reference to the Purchase Invoice.",
    )

    charge_type_id: Mapped[UUID] = mapped_column(
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
        doc="Calculated tax amount.",
    )

    line_total: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Net charge amount including tax.",
    )

    line_no: Mapped[int] = mapped_column(
        nullable=False,
    )

    # Relationships
    purchase_invoice: Mapped["PurchaseInvoice"] = relationship(back_populates="charges")

    def __repr__(self) -> str:
        return f"<PurchaseInvoiceCharge(invoice_id='{self.purchase_invoice_id}', total={self.line_total})>"