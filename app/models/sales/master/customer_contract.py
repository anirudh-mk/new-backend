from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
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

class CustomerContract(BaseModel):
    """
    Represents a commercial agreement between a Company and a Customer.

    Purpose:
        Customer Contracts define the agreed business terms under which
        goods or services are sold to a customer.

        A contract serves as the governing document for pricing,
        payment terms, delivery conditions, discounts,
        credit limits, warranties, service commitments,
        renewal periods, and other commercial obligations.

        Sales Quotations, Sales Orders, and Sales Invoices
        may reference a Customer Contract to automatically
        apply the agreed conditions.

    Examples:

        Annual Supply Agreement

            Customer
                ABC Supermarket

            Contract Value
                ₹25,000,000

            Validity
                01-Jan-2026
                31-Dec-2026

            Payment
                Net 30 Days

        Maintenance Contract

            Customer
                XYZ Hospital

            Contract Value
                ₹8,50,000

            Duration
                3 Years

        Export Agreement

            Customer
                Global Imports LLC

            Currency
                USD

            Delivery
                FOB Cochin

    Workflow:

                    Company
                       │
                       ▼
              Customer Contract
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      Sales Quote   Sales Order   Sales Invoice

    Benefits:

        • Centralizes customer agreements.
        • Eliminates repeated data entry.
        • Ensures pricing consistency.
        • Supports long-term agreements.
        • Supports contract renewals.
        • Supports service contracts.
        • Simplifies compliance.
        • Enables contract reporting.
        • Reduces pricing disputes.
        • Improves customer relationship management.

    Relationships:

                    Company
                       │
                       ▼
               Customer Contract
                       │
                       ▼
                    Customer

    Example:

        Contract No

            CNT-2026-0012

        Customer

            ABC Traders

        Validity

            01-Jan-2026
                    ↓
            31-Dec-2026

        Credit Limit

            ₹10,00,000

        Contract Value

            ₹45,00,000

    Notes:

        • One Customer may have multiple Contracts.
        • Only one Contract should normally be active
          for the same business purpose.
        • Contracts may be renewed.
        • Contracts may expire automatically.
        • Contracts may override default pricing.
        • Contracts may override payment terms.
        • Contracts may define delivery commitments.
        • Contracts are optional for Sales documents.

    This model is referenced throughout
    CRM,
    Customer Management,
    Sales,
    Quotation,
    Sales Order,
    Sales Invoice,
    Pricing,
    Contract Management,
    Customer Portal,
    and Reporting modules.
    """

    __tablename__ = "customer_contracts"

    company_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Reference to the Company that owns this contract.",
    )

    customer_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Reference to the Customer associated with this contract.",
    )

    contract_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="Unique contract number.",
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        doc="Title or name of the contract.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Detailed description of the agreement.",
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Contract effective date.",
    )

    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        doc="Contract expiry date.",
    )

    contract_value: Mapped[float | None] = mapped_column(
        Numeric(18, 2),
        nullable=True,
        doc="Total monetary value of the contract.",
    )

    credit_limit: Mapped[float | None] = mapped_column(
        Numeric(18, 2),
        nullable=True,
        doc="Maximum credit allowed under this contract.",
    )

    currency_code: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="INR",
        doc="Currency used for the contract.",
    )

    payment_terms: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        doc="Agreed payment terms for this contract.",
    )

    delivery_terms: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
        doc="Agreed delivery conditions (Incoterms or internal terms).",
    )

    renewal_allowed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether this contract can be renewed.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether the contract is currently active.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional remarks or notes related to the contract.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------


