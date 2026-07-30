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
    from app.models.sales.invoice.sales_invoice_item import SalesInvoiceItem


class SalesInvoiceItemTax(BaseModel):
    """
    Represents a Tax applied to an individual Sales Invoice Item.

    Purpose:
        Sales Invoice Item Tax stores the tax details
        applicable to each Sales Invoice line.

        Instead of storing tax information directly
        inside Sales Invoice Item, every tax component
        is stored as a separate record.

        This enables support for multiple taxes on a
        single invoice item, including GST, CGST,
        SGST, IGST, VAT, Sales Tax, CESS,
        Excise Duty, Service Tax, and other
        country-specific taxation rules.

        The values stored in this table are immutable
        snapshots copied from the Tax Master at the
        time the invoice is generated.

    Examples:

        Product

            Dell Laptop

        Taxes

            CGST
                9%

            SGST
                9%

        --------------------------------------

        Product

            Export Product

        Taxes

            IGST
                18%

        --------------------------------------

        Product

            UAE Product

        Taxes

            VAT
                5%

    Workflow:

            Sales Invoice
                    │
                    ▼
          Sales Invoice Item
                    │
                    ▼
       Sales Invoice Item Tax
                    │
                    ▼
          Accounts Receivable
                    │
                    ▼
             General Ledger

    Benefits:

        • Supports unlimited taxes per invoice item.
        • Supports GST.
        • Supports VAT.
        • Supports Sales Tax.
        • Supports compound taxes.
        • Supports inclusive taxes.
        • Preserves historical tax values.
        • Simplifies accounting integration.
        • Enables statutory compliance.
        • Improves financial reporting.

    Relationships:

          SalesInvoiceItem
                  │
                  ▼
        SalesInvoiceItemTax
                  │
                  ▼
              Tax Master

    Example:

        Product

            Dell Latitude 5450

        Tax

            CGST

        Rate

            9%

        Taxable Amount

            ₹52,000

        Tax Amount

            ₹4,680

    Notes:

        • One invoice item may contain multiple taxes.
        • Tax values are copied from Tax Master.
        • Historical tax records should never change.
        • Supports tax exemptions.
        • Supports compound taxation.
        • Used during GL posting.
        • Used during GST/VAT return generation.
        • Used for financial reporting.

    This model is referenced throughout
    Sales,
    Accounts Receivable,
    Accounting,
    Finance,
    Taxation,
    GST Reporting,
    VAT Reporting,
    Financial Reporting,
    and Compliance modules.
    """

    __tablename__ = "sales_invoice_item_taxes"

    sales_invoice_item_id: Mapped[UUID] = mapped_column(
        ForeignKey("sales_invoice_items.id"),
        nullable=False,
        index=True,
        doc="Reference to the Sales Invoice Item.",
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
        doc="Amount on which the tax is calculated.",
    )

    tax_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Calculated tax amount.",
    )

    is_inclusive: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether this tax is included in the unit price.",
    )

    sequence: Mapped[int] = mapped_column(
        nullable=False,
        default=1,
        doc="Calculation order for compound taxes.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    sales_invoice_item: Mapped["SalesInvoiceItem"] = relationship(
        back_populates="taxes",
    )

