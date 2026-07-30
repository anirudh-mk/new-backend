from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    Numeric,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    pass  # decoupled: from app.models.accounting.tax_type import TaxType
    from app.models.purchase.invoice.purchase_invoice_item import PurchaseInvoiceItem


class PurchaseInvoiceItemTax(BaseModel):
    """
    Represents an item-level tax calculation for a Purchase Invoice line item.
    """

    __tablename__ = "purchase_invoice_item_taxes"

    purchase_invoice_item_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_invoice_items.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Reference to the Purchase Invoice Item.",
    )

    tax_type_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Reference to the Tax Type (e.g. CGST, SGST, IGST).",
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

    is_inclusive: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        doc="Indicates whether the tax is inclusive of item unit price.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    line_no: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        doc="Line number within the tax details.",
    )

    # Relationships
    purchase_invoice_item: Mapped["PurchaseInvoiceItem"] = relationship(back_populates="taxes")

    def __repr__(self) -> str:
        return f"<PurchaseInvoiceItemTax(item_id='{self.purchase_invoice_item_id}', tax_amount={self.tax_amount})>"