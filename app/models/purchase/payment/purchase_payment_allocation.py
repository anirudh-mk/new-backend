from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.purchase.payment.purchase_payment import PurchasePayment
    from app.models.purchase.invoice.purchase_invoice import PurchaseInvoice


class PurchasePaymentAllocation(BaseModel):
    """
    Represents the allocation of a purchase payment to a specific purchase invoice.
    Supports many-to-many allocations between payments and invoices.
    """

    __tablename__ = "purchase_payment_allocations"

    payment_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_payments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Reference to the Purchase Payment.",
    )

    purchase_invoice_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_invoices.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Reference to the Purchase Invoice.",
    )

    allocated_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Amount allocated from the payment to the invoice.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Relationships
    payment: Mapped["PurchasePayment"] = relationship(back_populates="allocations")
    purchase_invoice: Mapped["PurchaseInvoice"] = relationship(back_populates="payments")

    def __repr__(self) -> str:
        return f"<PurchasePaymentAllocation(payment_id='{self.payment_id}', invoice_id='{self.purchase_invoice_id}', amount={self.allocated_amount})>"
