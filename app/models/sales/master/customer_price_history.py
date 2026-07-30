from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Date,
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
    from app.models.sales.master.customer_price import CustomerPrice


class CustomerPriceHistory(BaseModel):
    """
    Represents the historical audit trail of Customer Product Prices.

    Purpose:
        Customer Price History records every price revision made for a
        Customer Product Price.

        Instead of updating a Customer Price and losing the previous
        value, every modification creates a historical record,
        allowing organizations to trace pricing changes over time.

        This provides complete pricing transparency,
        supports auditing,
        enables rollback,
        and helps explain historical Sales Quotations,
        Sales Orders, and Sales Invoices.

    Examples:

        Product

            Dell Latitude Laptop

        Customer

            ABC Technologies

        Price Timeline

            01-Jan-2026
                ₹58,000

            15-Mar-2026
                ₹56,500

            01-Jul-2026
                ₹55,250

        -----------------------------------

        Product

            Printer

        Customer

            XYZ Industries

        Old Price

            ₹8,250

        New Price

            ₹7,950

        Reason

            Annual Contract Renewal

    Workflow:

                 Customer Price
                        │
             Price Updated
                        │
                        ▼
             Customer Price History
                        │
                        ▼
              Pricing Audit Report
                        │
                        ▼
              Historical Sales Analysis

    Benefits:

        • Complete audit trail.
        • Tracks every price revision.
        • Enables rollback.
        • Supports internal audits.
        • Explains historical invoices.
        • Maintains pricing transparency.
        • Supports contract negotiations.
        • Improves compliance.
        • Enables pricing trend analysis.
        • Preserves historical business data.

    Relationships:

                    Company
                       │
                       ▼
              Customer Price History
             ┌─────────┼──────────┐
             ▼         ▼          ▼
      CustomerPrice Customer Product
                               │
                               ▼
                        Product Variant

    Example:

        Customer

            ABC Traders

        Product

            HP Laptop

        Old Price

            ₹52,000

        New Price

            ₹50,500

        Changed On

            10-Apr-2026

        Reason

            Dealer Discount Revision

    Notes:

        • Records should never be updated.
        • Records should never be deleted.
        • One revision creates one history record.
        • Multiple revisions are stored chronologically.
        • Used only for reporting and auditing.
        • Does not participate in pricing calculations.
        • Supports unlimited history.
        • Historical records are immutable.

    This model is referenced throughout
    Pricing Engine,
    Customer Pricing,
    CRM,
    Sales,
    Audit,
    Reporting,
    Business Intelligence,
    Analytics,
    and Compliance modules.
    """

    __tablename__ = "customer_price_histories"

    company_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Reference to the Company.",
    )

    customer_price_id: Mapped[UUID] = mapped_column(
        ForeignKey("customer_prices.id"),
        nullable=False,
        index=True,
        doc="Reference to the Customer Price that was modified.",
    )

    customer_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Reference to the Customer.",
    )

    product_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Reference to the Product.",
    )

    product_variant_id: Mapped[UUID | None] = mapped_column(
        nullable=True,
        index=True,
        doc="Optional Product Variant associated with this price revision.",
    )

    old_price: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Selling price before the modification.",
    )

    new_price: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Selling price after the modification.",
    )

    changed_on: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Date on which the price revision became effective.",
    )

    reason: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        doc="Reason for changing the selling price.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional remarks regarding this price revision.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------





