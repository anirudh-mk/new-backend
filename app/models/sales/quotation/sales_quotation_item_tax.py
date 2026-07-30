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
    from app.models.sales.quotation.sales_quotation_item import SalesQuotationItem


class SalesQuotationItemTax(BaseModel):
    """
    Represents a Tax applied to a Sales Quotation Item.

    Purpose:
        Sales Quotation Item Tax stores the tax details applicable
        to an individual quotation line.

        A quotation item may have one or more taxes depending on
        the country's taxation rules.

        Examples include GST, CGST, SGST, IGST, VAT,
        Sales Tax, Excise Duty, Service Tax,
        Environmental Tax, and Luxury Tax.

        Keeping taxes in a separate table allows the ERP
        to support multiple tax components on a single
        quotation item without modifying the item model.

    Examples:

        Product

            Laptop

        Taxes

            CGST
                9%

            SGST
                9%

        --------------------------------------

        Product

            Export Item

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

            Sales Quotation
                    │
                    ▼
          Sales Quotation Item
                    │
                    ▼
       Sales Quotation Item Tax
                    │
                    ▼
             Tax Calculation
                    │
                    ▼
             Sales Order Item

    Benefits:

        • Supports unlimited taxes per item.
        • Supports GST.
        • Supports VAT.
        • Supports country-specific taxes.
        • Supports tax exemptions.
        • Supports future tax changes.
        • Simplifies tax reporting.
        • Enables accurate invoice generation.
        • Improves accounting integration.
        • Eliminates duplicated tax columns.

    Relationships:

            SalesQuotationItem
                    │
                    ▼
          SalesQuotationItemTax
                    │
                    ▼
                   Tax

    Example:

        Product

            Dell Laptop

        Tax

            CGST

        Percentage

            9%

        Tax Amount

            ₹4,680

    Notes:

        • One quotation item may contain multiple taxes.
        • Tax rates are copied from the Tax Master.
        • Historical tax values should never change.
        • Supports compound taxes.
        • Supports inclusive taxes.
        • Supports exclusive taxes.
        • Supports tax exemptions.
        • Supports regional tax rules.

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

    __tablename__ = "sales_quotation_item_taxes"

    quotation_item_id: Mapped[UUID] = mapped_column(
        ForeignKey("sales_quotation_items.id"),
        nullable=False,
        index=True,
        doc="Reference to the Sales Quotation Item.",
    )

    tax_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Reference to the Tax master.",
    )

    tax_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="Tax name copied from the Tax master for historical accuracy.",
    )

    tax_code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        doc="Tax code copied from the Tax master.",
    )

    tax_percentage: Mapped[Decimal] = mapped_column(
        Numeric(8, 4),
        nullable=False,
        doc="Applied tax percentage.",
    )

    taxable_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Amount on which tax is calculated.",
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
        doc="Indicates whether the tax is included in the unit price.",
    )

    sequence: Mapped[int] = mapped_column(
        nullable=False,
        default=1,
        doc="Calculation order for compound taxes.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    quotation_item: Mapped["SalesQuotationItem"] = relationship(
        back_populates="taxes",
    )

