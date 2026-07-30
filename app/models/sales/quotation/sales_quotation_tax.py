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
    from app.models.sales.quotation.sales_quotation import SalesQuotation


class SalesQuotationTax(BaseModel):
    """
    Represents a document-level Tax applied to a Sales Quotation.

    Purpose:
        Sales Quotation Tax stores the taxes applied to the
        overall quotation rather than individual quotation items.

        While most taxes are calculated per line item,
        certain jurisdictions or business requirements
        require taxes to be calculated on the entire document.

        This model also stores summarized tax information
        that appears in the quotation totals section.

    Examples:

        GST Summary

            Taxable Amount
                ₹1,00,000

            CGST
                ₹9,000

            SGST
                ₹9,000

        --------------------------------------

        Export Quotation

            IGST
                ₹18,000

        --------------------------------------

        VAT Summary

            VAT 5%
                ₹2,500

    Workflow:

            Sales Quotation
                    │
                    ▼
          Sales Quotation Tax
                    │
                    ▼
            Grand Total Calculation
                    │
                    ▼
               Sales Order
                    │
                    ▼
              Sales Invoice

    Benefits:

        • Supports document-level taxes.
        • Provides tax summary for printing.
        • Supports GST/VAT reporting.
        • Supports multiple tax components.
        • Supports inclusive/exclusive taxes.
        • Simplifies accounting integration.
        • Improves reporting accuracy.
        • Maintains historical tax values.
        • Enables statutory compliance.
        • Supports country-specific taxation.

    Relationships:

            SalesQuotation
                    │
                    ▼
           SalesQuotationTax
                    │
                    ▼
                  Tax Master

    Example:

        Tax

            CGST

        Tax Rate

            9%

        Taxable Amount

            ₹2,50,000

        Tax Amount

            ₹22,500

    Notes:

        • One quotation may contain multiple document taxes.
        • Tax values are copied from Tax Master.
        • Historical tax values should never change.
        • Used for quotation totals and reporting.
        • Item-level taxes remain stored separately.
        • Supports compound taxes.
        • Supports inclusive taxes.
        • Supports tax exemptions.

    This model is referenced throughout
    Sales,
    Taxation,
    Accounting,
    Sales Order,
    Sales Invoice,
    GST Reporting,
    VAT Reporting,
    Financial Reporting,
    and Compliance modules.
    """

    __tablename__ = "sales_quotation_taxes"

    quotation_id: Mapped[UUID] = mapped_column(
        ForeignKey("sales_quotations.id"),
        nullable=False,
        index=True,
        doc="Reference to the Sales Quotation.",
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
        doc="Calculated document tax amount.",
    )

    is_inclusive: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether this tax is included in the quotation total.",
    )

    sequence: Mapped[int] = mapped_column(
        nullable=False,
        default=1,
        doc="Calculation order for compound taxes.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    quotation: Mapped["SalesQuotation"] = relationship(
        back_populates="taxes",
    )

