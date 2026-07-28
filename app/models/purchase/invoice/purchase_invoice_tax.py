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
    from app.models.purchase.invoice.purchase_invoice import PurchaseInvoice


class PurchaseInvoiceTax(BaseModel):
    """
    Represents a tax applied to a Purchase Invoice.

    Purpose:
        Purchase Invoice Tax stores document-level tax details applied
        to a Purchase Invoice. Multiple tax records may exist for a
        single invoice, allowing support for GST, VAT, TCS, customs,
        and other tax structures.

        These records are used for tax reporting, accounting entries,
        and statutory compliance.

    Examples:

        • CGST
        • SGST
        • IGST
        • VAT
        • Service Tax
        • TCS
        • Customs Duty

    Benefits:

        • Supports multiple taxes
        • Easy GST/VAT reporting
        • Accounting integration
        • Tax audit compliance
        • Financial reporting

    Relationships:

        PurchaseInvoice
                │
                └── PurchaseInvoiceTax

        TaxType
                │
                └── PurchaseInvoiceTax
    """

    __tablename__ = "purchase_invoice_taxes"

    purchase_invoice_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_invoices.id"),
        nullable=False,
        index=True,
        doc="Reference to the Purchase Invoice.",
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
        doc="Line number within the Purchase Invoice tax section.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    purchase_invoice: Mapped["PurchaseInvoice"] = relationship(
        back_populates="taxes",
    )

    tax_type: Mapped["TaxType"] = relationship()