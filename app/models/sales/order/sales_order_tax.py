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
    from app.models.sales.order.sales_order import SalesOrder


class SalesOrderTax(BaseModel):
    """
    Represents a document-level Tax applied to a Sales Order.

    Purpose:
        Sales Order Tax stores taxes that are applied at the
        overall Sales Order level.

        Although most taxes are calculated for each line item,
        many countries require a summarized document-level tax
        breakdown for statutory reporting, accounting,
        invoice generation, and customer documents.

        This model stores a snapshot of each tax component
        applicable to the Sales Order.

    Examples:

        GST Summary

            Taxable Amount
                ₹1,50,000

            CGST
                ₹13,500

            SGST
                ₹13,500

        --------------------------------------

        Export Order

            IGST
                ₹27,000

        --------------------------------------

        UAE Order

            VAT
                ₹7,500

    Workflow:

              Sales Order
                   │
                   ▼
            Sales Order Tax
                   │
                   ▼
            Invoice Generation
                   │
                   ▼
             Accounting Entry

    Benefits:

        • Supports multiple document taxes.
        • Supports GST.
        • Supports VAT.
        • Supports Sales Tax.
        • Supports compound taxes.
        • Supports inclusive taxes.
        • Simplifies reporting.
        • Improves statutory compliance.
        • Preserves historical tax values.
        • Enables financial reconciliation.

    Relationships:

             SalesOrder
                  │
                  ▼
            SalesOrderTax
                  │
                  ▼
               Tax Master

    Example:

        Tax

            CGST

        Rate

            9%

        Taxable Amount

            ₹2,00,000

        Tax Amount

            ₹18,000

    Notes:

        • One Sales Order may contain multiple document taxes.
        • Tax details are copied from the Tax Master.
        • Historical tax values should never change.
        • Used for invoice generation.
        • Used for GST/VAT reporting.
        • Supports compound tax calculation.
        • Supports country-specific taxation.
        • Item-level taxes are maintained separately.

    This model is referenced throughout
    Sales,
    Accounting,
    Taxation,
    Sales Invoice,
    GST Reporting,
    VAT Reporting,
    Financial Reporting,
    Compliance,
    and Analytics modules.
    """

    __tablename__ = "sales_order_taxes"

    sales_order_id: Mapped[UUID] = mapped_column(
        ForeignKey("sales_orders.id"),
        nullable=False,
        index=True,
        doc="Reference to the Sales Order.",
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
        doc="Calculated document-level tax amount.",
    )

    is_inclusive: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether the tax is included in the order total.",
    )

    sequence: Mapped[int] = mapped_column(
        nullable=False,
        default=1,
        doc="Calculation sequence for compound taxes.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    sales_order: Mapped["SalesOrder"] = relationship(
        back_populates="taxes",
    )

