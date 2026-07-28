from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.company.company import Company
    from app.models.purchase.invoice.purchase_invoice import PurchaseInvoice


class PurchaseInvoiceType(BaseModel):
    """
    Defines the various types of Purchase Invoices.

    Purpose:
        Purchase Invoice Types categorize supplier invoices based on
        business scenarios. Instead of hardcoding invoice categories,
        this configurable master allows organizations to create and
        maintain invoice types according to their procurement and
        accounting policies.

        Purchase Invoice Types are useful for reporting, approval
        workflows, taxation, and financial analysis.

    Common Types:

        • Regular
            Standard supplier purchase invoice.

        • Import
            Invoice related to imported goods.

        • Service
            Invoice for purchased services.

        • Debit Note
            Additional amount payable to supplier.

        • Credit Adjustment
            Adjustment reducing supplier payable.

        • Opening Balance
            Initial supplier balance migrated into ERP.

        • Expense
            Direct expense invoice without inventory impact.

    Example:

        Purchase Order
              │
              ▼
        Purchase Receipt
              │
              ▼
        Purchase Invoice
              │
        Invoice Type = Regular

    Benefits:
        • Configurable invoice categories
        • Supports accounting workflows
        • Simplifies reporting
        • Enables approval routing
        • Supports financial analytics
        • Easy to extend without code changes

    Relationships:

        PurchaseInvoiceType
                │
                └── PurchaseInvoice
    """

    __tablename__ = "purchase_invoice_types"

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "code",
            name="uq_purchase_invoice_type_company_code",
        ),
    )

    company_id: Mapped[int | None] = mapped_column(
        ForeignKey("companies.id"),
        nullable=True,
        index=True,
        doc="Company owning this invoice type. NULL indicates a global invoice type.",
    )

    code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        doc="Unique purchase invoice type code.",
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="Purchase invoice type name.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Detailed description of the purchase invoice type.",
    )

    affects_inventory: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether invoices of this type affect inventory valuation.",
    )

    affects_accounts_payable: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether this invoice type creates or adjusts Accounts Payable.",
    )

    is_system: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether this is a predefined system invoice type.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether this invoice type is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    company: Mapped["Company"] = relationship()

    purchase_invoices: Mapped[list["PurchaseInvoice"]] = relationship(
        back_populates="invoice_type",
    )