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
    from app.models.sales.order.sales_order import SalesOrder


class SalesOrderCharge(BaseModel):
    """
    Represents an additional Charge applied to a Sales Order.

    Purpose:
        Sales Order Charge stores document-level charges
        that are applied to the entire Sales Order rather
        than to individual order items.

        These charges contribute to the final payable amount
        and are copied to downstream documents such as
        Delivery Notes and Sales Invoices.

        Common examples include freight,
        transportation, insurance,
        packaging, installation,
        documentation, loading,
        unloading, handling,
        and miscellaneous service charges.

    Examples:

        Freight
            ₹3,500

        Insurance
            ₹1,200

        Packing Charge
            ₹850

        Installation
            ₹5,000

        Documentation
            ₹400

    Workflow:

              Sales Order
                    │
                    ▼
          Sales Order Charge
                    │
                    ▼
         Grand Total Calculation
                    │
                    ▼
            Sales Invoice
                    │
                    ▼
            Accounting Entry

    Benefits:

        • Supports unlimited charges.
        • Supports freight charges.
        • Supports transportation charges.
        • Supports insurance charges.
        • Supports installation charges.
        • Supports percentage-based charges.
        • Supports fixed amount charges.
        • Supports taxable charges.
        • Improves pricing flexibility.
        • Maintains historical charge values.

    Relationships:

             SalesOrder
                  │
                  ▼
          SalesOrderCharge

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

        • One Sales Order may contain multiple charges.
        • Charges may be taxable.
        • Charges may be fixed amounts.
        • Charges may be percentage based.
        • Charges are copied to Sales Invoice.
        • Charges are copied to accounting entries.
        • Historical values should never change.
        • Used during final total calculation.

    This model is referenced throughout
    Sales,
    Pricing,
    Inventory,
    Shipping,
    Accounting,
    Financial Reporting,
    Analytics,
    and Customer Billing modules.
    """

    __tablename__ = "sales_order_charges"

    sales_order_id: Mapped[UUID] = mapped_column(
        ForeignKey("sales_orders.id"),
        nullable=False,
        index=True,
        doc="Reference to the Sales Order.",
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
        doc="Percentage value when using percentage-based calculation.",
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
        doc="Indicates whether the charge is taxable.",
    )

    included_in_total: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether the charge contributes to the Sales Order grand total.",
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

    sales_order: Mapped["SalesOrder"] = relationship(
        back_populates="charges",
    )