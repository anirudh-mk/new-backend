from __future__ import annotations

from datetime import date
from decimal import Decimal
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

if TYPE_CHECKING:
    from app.models.sales.master.sales_person import SalesPerson
    from app.models.sales.master.sales_terms import SalesTerms
    from app.models.sales.master.sales_price_list import SalesPriceList
    from app.models.workflow.approval_workflow import ApprovalWorkflow
    from app.models.sales.quotation.sales_quotation_item import SalesQuotationItem


class SalesQuotation(BaseModel):
    """
    Represents a Sales Quotation issued to a Customer.

    Purpose:
        A Sales Quotation is a formal commercial offer provided
        to a customer before a Sales Order is created.

        It defines the proposed products, quantities,
        selling prices, taxes, discounts,
        delivery information,
        payment terms,
        quotation validity,
        and commercial conditions.

        Once accepted,
        a Sales Quotation may be converted into
        a Sales Order.

    Examples:

        Customer

            ABC Supermarket

        Products

            Rice
            Sugar
            Cooking Oil

        Valid Until

            30-Jun-2026

        Grand Total

            ₹2,35,450

    Workflow:

            Lead
              │
              ▼
        Opportunity
              │
              ▼
       Sales Quotation
              │
              ▼
         Customer Review
              │
      ┌───────┴────────┐
      ▼                ▼
    Rejected        Accepted
                       │
                       ▼
                 Sales Order

    Benefits:

        • Professional customer proposals.
        • Multiple revisions.
        • Approval workflow.
        • Automatic order creation.
        • Tax calculation.
        • Discount management.
        • Validity tracking.
        • Customer negotiation.
        • Sales forecasting.
        • Profit estimation.

    Relationships:

                Company
                   │
                   ▼
            SalesQuotation
         ┌─────┼─────┬─────┐
         ▼     ▼     ▼     ▼
    Customer Branch SalesPerson
                   │
                   ▼
          SalesQuotationItem

    Notes:

        • One quotation has many quotation items.
        • May be revised multiple times.
        • May expire automatically.
        • Can be partially converted to Sales Orders.
        • Can be cancelled.
        • Supports approval workflow.
        • Supports multiple currencies.
        • Supports multiple taxes.
        • Historical quotations remain unchanged.

    This model is referenced throughout
    CRM,
    Sales,
    Order Management,
    Inventory,
    Pricing,
    Approval Workflow,
    Reporting,
    Customer Portal,
    and Analytics modules.
    """

    __tablename__ = "sales_quotations"

    quotation_number: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
        index=True,
        doc="Unique quotation number.",
    )

    company_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Company issuing the quotation.",
    )

    branch_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Branch issuing the quotation.",
    )

    customer_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Customer receiving the quotation.",
    )

    sales_person_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("sales_persons.id"),
        nullable=True,
        index=True,
        doc="Assigned Sales Person.",
    )

    sales_price_list_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("sales_price_lists.id"),
        nullable=True,
        index=True,
        doc="Applied Sales Price List.",
    )

    sales_terms_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("sales_terms.id"),
        nullable=True,
        index=True,
        doc="Applied Sales Terms.",
    )

    approval_workflow_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("approval_workflows.id"),
        nullable=True,
        index=True,
        doc="Approval workflow assigned to this quotation.",
    )

    quotation_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Quotation date.",
    )

    valid_until: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        doc="Quotation validity date.",
    )

    currency_code: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="INR",
        doc="Currency code.",
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Total before discounts and taxes.",
    )

    discount_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Document discount.",
    )

    tax_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Total tax amount.",
    )

    other_charges: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Shipping, packing or other charges.",
    )

    grand_total: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Final quotation value.",
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="DRAFT",
        doc="Quotation status.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Internal remarks.",
    )

    customer_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Notes printed for the customer.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        doc="Indicates whether the quotation is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------




    sales_person: Mapped["SalesPerson"] = relationship(
        back_populates="quotations"
    )

    sales_price_list: Mapped["SalesPriceList"] = relationship()

    sales_terms: Mapped["SalesTerms"] = relationship()

    approval_workflow: Mapped["ApprovalWorkflow"] = relationship()

    items: Mapped[list["SalesQuotationItem"]] = relationship(
        back_populates="quotation",
        cascade="all, delete-orphan",
    )