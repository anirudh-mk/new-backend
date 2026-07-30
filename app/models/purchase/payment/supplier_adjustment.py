from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Date,
    ForeignKey,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    pass  # decoupled: from app.models.company.company.company import Company
    pass  # decoupled: from app.models.company.company.branch import Branch
    pass  # decoupled: from app.models.party.party import Party
    from app.models.purchase.payment.supplier_debit_note import SupplierDebitNote
    from app.models.purchase.invoice.purchase_invoice import PurchaseInvoice
    pass  # decoupled: from app.models.user.user import User


class SupplierAdjustment(AuditModel):
    """
    Represents adjustments applied to offset debit notes against purchase invoices or write-offs.
    """

    __tablename__ = "supplier_adjustments"

    company_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
    )

    branch_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
    )

    supplier_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
    )

    adjustment_no: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
        doc="Unique adjustment entry number.",
    )

    adjustment_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    debit_note_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("supplier_debit_notes.id"),
        nullable=True,
        index=True,
        doc="The supplier debit note being adjusted or applied.",
    )

    purchase_invoice_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("purchase_invoices.id"),
        nullable=True,
        index=True,
        doc="The purchase invoice against which the debit note or adjustment is applied.",
    )

    adjustment_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Amount being adjusted.",
    )

    adjustment_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        doc="Type of adjustment (e.g. Write-off, Refund, Invoice Offset).",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    adjusted_by_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="User who logged the adjustment.",
    )

    # Relationships
    debit_note: Mapped["SupplierDebitNote"] = relationship()
    purchase_invoice: Mapped["PurchaseInvoice"] = relationship()

    def __repr__(self) -> str:
        return f"<SupplierAdjustment(adjustment_no='{self.adjustment_no}', amount={self.adjustment_amount})>"