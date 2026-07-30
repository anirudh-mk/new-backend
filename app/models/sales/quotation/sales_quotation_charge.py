from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.sales.quotation.sales_quotation import SalesQuotation


class SalesQuotationCharge(BaseModel):
    """
    Represents an additional Charge applied to a Sales Quotation.

    Purpose:
        Sales Quotation Charge stores document-level charges
        that are applied in addition to the quoted products.

        These charges are not tied to a specific quotation item.
        Instead, they apply to the quotation as a whole and
        contribute to the final quotation value.

        Typical examples include freight, packing,
        insurance, loading, unloading, documentation,
        installation, handling, and miscellaneous service charges.

        Multiple charges may be added to a single quotation.

    Examples:

        Freight
            ₹2,500

        Packing
            ₹850

        Insurance
            ₹1,250

        Documentation Charge
            ₹500

        Installation Charge
            ₹4,000

    Workflow:

              Sales Quotation
                     │
                     ▼
          Sales Quotation Charge
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

        • Supports unlimited additional charges.
        • Supports freight charges.
        • Supports packing charges.
        • Supports insurance charges.
        • Supports installation charges.
        • Supports handling charges.
        • Supports percentage-based charges.
        • Supports fixed amount charges.
        • Improves quotation flexibility.
        • Simplifies document calculations.

    Relationships:

             SalesQuotation
                    │
                    ▼
          SalesQuotationCharge

    Example:

        Charge

            Freight

        Type

            Fixed Amount

        Amount

            ₹2,500

        Taxable

            Yes

    Notes:

        • One quotation may contain multiple charges.
        • Charges may be taxable.
        • Charges may be percentage based.
        • Charges may be fixed amounts.
        • Charges are copied to Sales Orders.
        • Charges are copied to Sales Invoices.
        • Historical charges should never change.
        • Used during total calculation.

    This model is referenced throughout
    Sales,
    Pricing,
    Taxation,
    Sales Order,
    Sales Invoice,
    Accounting,
    Reporting,
    Analytics,
    and Financial modules.
    """

    __tablename__ = "sales_quotation_charges"

    quotation_id: Mapped[UUID] = mapped_column(
        ForeignKey("sales_quotations.id"),
        nullable=False,
        index=True,
        doc="Reference to the Sales Quotation.",
    )

    charge_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="Display name of the charge.",
    )

    charge_code: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
        index=True,
        doc="Optional unique charge code.",
    )

    calculation_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="FIXED",
        doc="Calculation method (FIXED or PERCENTAGE).",
    )

    percentage: Mapped[Decimal] = mapped_column(
        Numeric(8, 4),
        nullable=False,
        default=0,
        doc="Percentage value when calculation type is PERCENTAGE.",
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Calculated or manually entered charge amount.",
    )

    taxable: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether this charge is taxable.",
    )

    included_in_total: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether the charge contributes to the quotation grand total.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional remarks about this charge.",
    )

    sequence: Mapped[int] = mapped_column(
        nullable=False,
        default=1,
        doc="Display and calculation order of the charge.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    quotation: Mapped["SalesQuotation"] = relationship(
        back_populates="charges",
    )