from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.sales.invoice.sales_invoice import SalesInvoice


class SalesInvoiceTax(BaseModel):
    """
    Represents a document-level Tax applied to a Sales Invoice.

    Purpose:
        Sales Invoice Tax stores the summarized tax
        components applicable to the entire Sales Invoice.

        While taxes are normally calculated at the
        individual invoice item level, this table stores
        the consolidated tax breakdown required for
        accounting, statutory reporting,
        invoice printing, and customer billing.

        Each record represents one tax component such as
        CGST, SGST, IGST, VAT, Sales Tax,
        Excise Duty, Service Tax,
        or other country-specific taxes.

        Tax values stored here are immutable snapshots
        copied from the Tax Master during invoice creation.

    Examples:

        GST Summary

            Taxable Amount
                ₹2,50,000

            CGST
                ₹22,500

            SGST
                ₹22,500

        --------------------------------------

        Export Invoice

            IGST
                ₹45,000

        --------------------------------------

        UAE Invoice

            VAT
                ₹12,500

    Workflow:

            Sales Invoice
                   │
                   ▼
          Sales Invoice Tax
                   │
                   ▼
         Accounts Receivable
                   │
                   ▼
            General Ledger
                   │
                   ▼
          GST / VAT Returns

    Benefits:

        • Supports multiple document taxes.
        • Supports GST.
        • Supports VAT.
        • Supports Sales Tax.
        • Supports compound taxation.
        • Supports inclusive taxes.
        • Preserves historical tax values.
        • Simplifies invoice printing.
        • Enables statutory reporting.
        • Improves financial reconciliation.

    Relationships:

             SalesInvoice
                   │
                   ▼
           SalesInvoiceTax
                   │
                   ▼
               Tax Master

    Example:

        Tax

            CGST

        Rate

            9%

        Taxable Amount

            ₹2,50,000

        Tax Amount

            ₹22,500

    Notes:

        • One invoice may contain multiple tax components.
        • Tax values are copied from Tax Master.
        • Historical tax values should never change.
        • Used for invoice totals.
        • Used for GST/VAT reporting.
        • Supports compound taxes.
        • Supports tax exemptions.
        • Item-level taxes remain stored separately.

    This model is referenced throughout
    Sales,
    Accounts Receivable,
    Accounting,
    Finance,
    Taxation,
    GST Reporting,
    VAT Reporting,
    Financial Reporting,
    Compliance,
    and Analytics modules.
    """

    __tablename__ = "sales_invoice_taxes"

    sales_invoice_id: Mapped[UUID] = mapped_column(
        ForeignKey("sales_invoices.id"),
        nullable=False,
        index=True,
        doc="Reference to the Sales Invoice.",
    )

    tax_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Reference to the Tax Master.",
    )

    tax_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="Tax name copied from the Tax Master.",
    )

    tax_code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        doc="Tax code copied from the Tax Master.",
    )

    tax_percentage: Mapped[Decimal] = mapped_column(
        Numeric(8, 4),
        nullable=False,
        doc="Applied tax percentage.",
    )

    taxable_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Document taxable amount.",
    )

    tax_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Calculated document-level tax amount.",
    )

    is_inclusive: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether the tax is included in the invoice total.",
    )

    sequence: Mapped[int] = mapped_column(
        nullable=False,
        default=1,
        doc="Calculation order for compound taxes.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    sales_invoice: Mapped["SalesInvoice"] = relationship(
        back_populates="taxes",
    )

