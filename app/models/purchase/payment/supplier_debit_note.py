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

from app.database.base import AuditModel, BaseModel

if TYPE_CHECKING:
    pass  # decoupled: from app.models.company.company.company import Company
    pass  # decoupled: from app.models.company.company.branch import Branch
    pass  # decoupled: from app.models.party.party import Party
    from app.models.purchase.returns.purchase_return import PurchaseReturn
    pass  # decoupled: from app.models.core.currency import Currency
    pass  # decoupled: from app.models.accounting.journal_status import JournalStatus
    from app.models.purchase.returns.purchase_return_item import PurchaseReturnItem
    from app.models.inventory.product.product import Product
    from app.models.inventory.product.product_variant import ProductVariant
    from app.models.inventory.uom.uom import UOM


class SupplierDebitNote(AuditModel):
    """
    Represents a Supplier Debit Note issued for returns or price corrections.
    """

    __tablename__ = "supplier_debit_notes"

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

    purchase_return_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("purchase_returns.id"),
        nullable=True,
        index=True,
        doc="Reference to the linked Purchase Return if any.",
    )

    debit_note_no: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
        doc="Unique Debit Note number.",
    )

    debit_note_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Date on which the Debit Note was issued.",
    )

    currency_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
    )

    exchange_rate: Mapped[float] = mapped_column(
        Numeric(18, 6),
        nullable=False,
        default=1,
    )

    subtotal: Mapped[float] = mapped_column(
        Numeric(18, 2),
        default=0,
    )

    tax_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        default=0,
    )

    other_charges: Mapped[float] = mapped_column(
        Numeric(18, 2),
        default=0,
    )

    grand_total: Mapped[float] = mapped_column(
        Numeric(18, 2),
        default=0,
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
    )

    # Relationships
    purchase_return: Mapped["PurchaseReturn"] = relationship()

    items: Mapped[list["SupplierDebitNoteItem"]] = relationship(
        back_populates="debit_note",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<SupplierDebitNote(debit_note_no='{self.debit_note_no}', grand_total={self.grand_total})>"


class SupplierDebitNoteItem(BaseModel):
    """
    Represents an item row within a Supplier Debit Note.
    """

    __tablename__ = "supplier_debit_note_items"

    debit_note_id: Mapped[UUID] = mapped_column(
        ForeignKey("supplier_debit_notes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    purchase_return_item_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("purchase_return_items.id"),
        nullable=True,
        index=True,
    )

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )

    variant_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("product_variants.id"),
        nullable=True,
        index=True,
    )

    uom_id: Mapped[UUID] = mapped_column(
        ForeignKey("uoms.id"),
        nullable=False,
        index=True,
    )

    quantity: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
    )

    unit_price: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
    )

    tax_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
    )

    line_total: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    line_no: Mapped[int] = mapped_column(
        nullable=False,
    )

    # Relationships
    debit_note: Mapped["SupplierDebitNote"] = relationship(back_populates="items")
    purchase_return_item: Mapped["PurchaseReturnItem"] = relationship()
    product: Mapped["Product"] = relationship()
    variant: Mapped["ProductVariant"] = relationship()
    uom: Mapped["UOM"] = relationship()

    def __repr__(self) -> str:
        return f"<SupplierDebitNoteItem(debit_note_id='{self.debit_note_id}', line_no={self.line_no})>"