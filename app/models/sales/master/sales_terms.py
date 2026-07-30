from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
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
    from app.models.company.company import Company
    from app.models.sales.quotation.sales_quotation import SalesQuotation
    from app.models.sales.order.sales_order import SalesOrder
    from app.models.sales.invoice.sales_invoice import SalesInvoice


class SalesTerms(BaseModel):
    """
    Represents reusable Sales Terms and Conditions.

    Purpose:
        Sales Terms define the legal, commercial, payment, warranty,
        delivery, cancellation, and other conditions applicable to
        sales transactions.

        Instead of manually typing terms for every quotation,
        sales order, or invoice, users can maintain reusable
        Sales Terms templates and simply attach one to a document.

        This improves consistency, reduces manual work,
        and ensures legal compliance across the organization.

    Usage:

        Sales Terms can be attached to:

            • Sales Quotation
            • Sales Order
            • Delivery Note (Optional)
            • Sales Invoice

        When a Sales document is created, the selected Sales Terms
        become part of the generated document and are printed
        in PDF reports.

    Examples:

        Standard Terms

            • Goods once sold cannot be returned.
            • Payment due within 30 days.
            • Warranty as per manufacturer policy.
            • Subject to Kerala jurisdiction.

        Cash Sale

            • Payment must be received before delivery.
            • No credit allowed.
            • Delivery after payment confirmation.

        Export Terms

            • FOB Cochin Port.
            • Payment through Letter of Credit.
            • Customs clearance by buyer.

        Retail Invoice

            • No warranty on discounted items.
            • Exchange allowed within 7 days.
            • Original invoice mandatory.

    Workflow:

                     Sales Terms
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
     Sales Quotation   Sales Order   Sales Invoice
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                   Printed Documents

    Benefits:

        • Centralized management of legal terms.
        • Eliminates duplicate typing.
        • Ensures company-wide consistency.
        • Supports multiple business scenarios.
        • Simplifies quotation generation.
        • Simplifies invoice generation.
        • Enables customer-specific templates.
        • Supports export and domestic sales.
        • Easy to update company policies.
        • Improves compliance.

    Relationships:

                    Company
                       │
                       ▼
                  SalesTerms
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      SalesQuotation  SalesOrder  SalesInvoice

    Example:

        Code

            STD

        Name

            Standard Terms

        Terms

            1. Payment due within 30 days.
            2. Goods once sold cannot be returned.
            3. Warranty as per manufacturer policy.
            4. Interest @18% per annum on overdue payments.
            5. Subject to Kozhikode jurisdiction.

    Notes:

        • Terms are maintained once and reused.
        • Documents may override the template if required.
        • One Company can maintain multiple Sales Terms.
        • Only one Sales Term may be marked as default.
        • Sales Terms do not affect accounting entries.
        • Sales Terms do not affect inventory.
        • Sales Terms are printable only.
        • Can be localized into multiple languages.

    This model is referenced throughout
    Sales, CRM, Customer Portal,
    Quotation Management,
    Order Management,
    Invoice Generation,
    Reporting,
    and Document Printing modules.
    """

    __tablename__ = "sales_terms"

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
        doc="Reference to the Company that owns this Sales Terms template.",
    )

    code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
        doc="Unique code identifying the Sales Terms template.",
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
        doc="Display name of the Sales Terms template.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Optional description explaining the purpose of this Sales Terms template.",
    )

    terms_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        doc="Complete Terms and Conditions text that will appear on Sales documents.",
    )

    is_default: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether this template is the default Sales Terms for new Sales documents.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether this Sales Terms template is active and available for selection.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    company: Mapped["Company"] = relationship(
        back_populates="sales_terms",
    )

    quotations: Mapped[list["SalesQuotation"]] = relationship(
        back_populates="sales_terms",
    )

    sales_orders: Mapped[list["SalesOrder"]] = relationship(
        back_populates="sales_terms",
    )

    sales_invoices: Mapped[list["SalesInvoice"]] = relationship(
        back_populates="sales_terms",
    )