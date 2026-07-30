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
    from app.models.sales.order.sales_order_item import SalesOrderItem


class SalesOrderItemTax(BaseModel):
    """
    Represents a Tax applied to an individual Sales Order Item.

    Purpose:
        Sales Order Item Tax stores the tax components applicable
        to each Sales Order Item.

        Instead of storing tax information directly inside
        Sales Order Item, every tax component is stored
        as an individual record.

        This architecture supports multiple taxes
        on a single line item including GST,
        CGST, SGST, IGST, VAT, CESS,
        Excise Duty, Service Tax,
        Environmental Tax,
        and other country-specific taxes.

        The values stored here are snapshots of the
        tax configuration at the time of order creation,
        ensuring historical accuracy.

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

             Sales Order
                   │
                   ▼
           Sales Order Item
                   │
                   ▼
        Sales Order Item Tax
                   │
                   ▼
          Sales Invoice Item
                   │
                   ▼
             Journal Entry

    Benefits:

        • Supports unlimited taxes per item.
        • Supports GST/VAT.
        • Supports tax snapshots.
        • Supports inclusive taxes.
        • Supports exclusive taxes.
        • Supports compound taxes.
        • Improves accounting integration.
        • Enables statutory reporting.
        • Supports tax audit.
        • Preserves historical values.

    Relationships:

            SalesOrderItem
                   │
                   ▼
        SalesOrderItemTax
                   │
                   ▼
                Tax Master

    Example:

        Product

            Dell Latitude

        Tax

            CGST

        Percentage

            9%

        Taxable Amount

            ₹52,000

        Tax Amount

            ₹4,680

    Notes:

        • One Sales Order Item may contain multiple taxes.
        • Tax Master values are copied during order creation.
        • Historical records should never change.
        • Supports multiple jurisdictions.
        • Supports tax exemptions.
        • Supports compound tax calculation.
        • Supports future tax revisions.
        • Used for invoice generation and accounting.

    This model is referenced throughout
    Sales,
    Inventory,
    Accounting,
    Taxation,
    Sales Invoice,
    GST Reporting,
    VAT Reporting,
    Compliance,
    and Financial Reporting modules.
    """

    __tablename__ = "sales_order_item_taxes"

    sales_order_item_id: Mapped[UUID] = mapped_column(
        ForeignKey("sales_order_items.id"),
        nullable=False,
        index=True,
        doc="Reference to the Sales Order Item.",
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
        doc="Calculation sequence for compound taxes.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    sales_order_item: Mapped["SalesOrderItem"] = relationship(
        back_populates="taxes",
    )

