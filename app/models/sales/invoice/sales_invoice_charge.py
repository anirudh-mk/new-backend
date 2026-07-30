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
    from app.models.sales.invoice.sales_invoice import SalesInvoice


class SalesInvoiceCharge(BaseModel):
    """
    Represents an additional Charge applied to a Sales Invoice.

    Purpose:
        Sales Invoice Charge stores document-level charges
        that are applied to the entire Sales Invoice.

        These charges are independent of invoice line items
        and contribute to the final invoice value.

        Typical examples include freight,
        transportation, insurance,
        packaging, installation,
        documentation, handling,
        loading, unloading,
        and miscellaneous service charges.

        Charges are normally copied from the
        originating Sales Order or Delivery Note,
        but they may also be added directly
        during invoice creation.

    Examples:

        Freight
            ₹3,500

        Insurance
            ₹1,250

        Installation
            ₹5,000

        Packing Charge
            ₹850

        Documentation
            ₹400

    Workflow:

            Sales Order
                  │
                  ▼
           Delivery Note
                  │
                  ▼
          Sales Invoice Charge
                  │
                  ▼
          Grand Total Calculation
                  │
                  ▼
        Accounts Receivable
                  │
                  ▼
            General Ledger

    Benefits:

        • Supports unlimited charges.
        • Supports freight.
        • Supports transportation.
        • Supports insurance.
        • Supports installation.
        • Supports handling charges.
        • Supports percentage-based charges.
        • Supports fixed amount charges.
        • Supports taxable charges.
        • Preserves historical values.

    Relationships:

             SalesInvoice
                  │
                  ▼
         SalesInvoiceCharge

    Example:

        Charge

            Freight

        Type

            Fixed Amount

        Amount

            ₹3,500

        Taxable

            Yes

    Notes:

        • One invoice may contain multiple charges.
        • Charges may be taxable.
        • Charges may be copied from Sales Orders.
        • Charges may be copied from Delivery Notes.
        • Historical values should never change.
        • Used during invoice total calculation.
        • Used for customer billing.
        • Used for accounting postings.

    This model is referenced throughout
    Sales,
    Accounts Receivable,
    Accounting,
    Finance,
    Taxation,
    Customer Billing,
    Financial Reporting,
    Analytics,
    and Compliance modules.
    """

    __tablename__ = "sales_invoice_charges"

    sales_invoice_id: Mapped[UUID] = mapped_column(
        ForeignKey("sales_invoices.id"),
        nullable=False,
        index=True,
        doc="Reference to the Sales Invoice.",
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
        doc="Optional charge code copied from the Charge Master.",
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
        doc="Indicates whether this charge contributes to the invoice grand total.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional remarks about this charge.",
    )

    sequence: Mapped[int] = mapped_column(
        nullable=False,
        default=1,
        doc="Display and calculation sequence of the charge.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    sales_invoice: Mapped["SalesInvoice"] = relationship(
        back_populates="charges",
    )