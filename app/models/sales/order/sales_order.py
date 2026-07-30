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
    from app.models.sales.quotation.sales_quotation import SalesQuotation
    from app.models.workflow.approval_workflow import ApprovalWorkflow
    from app.models.sales.order.sales_order_item import SalesOrderItem


class SalesOrder(BaseModel):
    """
    Represents a confirmed Sales Order received from a Customer.

    Purpose:
        A Sales Order is a legally accepted customer order
        confirming the purchase of goods or services.

        It is the primary operational document used for
        inventory reservation, delivery planning,
        shipment processing, invoicing,
        production planning (if applicable),
        and revenue recognition.

        A Sales Order may originate from a Sales Quotation
        or be created directly.

    Examples:

        Customer

            ABC Supermarket

        Order

            SO-2026-000125

        Products

            Rice
            Sugar
            Cooking Oil

        Total

            ₹3,45,250

    Workflow:

            Sales Quotation
                   │
                   ▼
              Sales Order
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
    Reservation Delivery   Invoice
                   │
                   ▼
             Customer Receipt

    Benefits:

        • Central sales document.
        • Inventory reservation.
        • Delivery planning.
        • Invoice generation.
        • Partial deliveries.
        • Partial invoicing.
        • Approval workflow.
        • Customer tracking.
        • Revenue forecasting.
        • Complete audit trail.

    Relationships:

                 Company
                    │
                    ▼
               SalesOrder
        ┌────────┼────────┬────────┐
        ▼        ▼        ▼        ▼
    Customer  Branch  SalesPerson Quotation
                    │
                    ▼
              SalesOrderItem

    Notes:

        • One order contains many items.
        • One quotation may create multiple orders.
        • Orders may be partially delivered.
        • Orders may be partially invoiced.
        • Orders may be cancelled.
        • Historical orders remain immutable.
        • Supports approval workflow.
        • Supports multi-currency.

    This model is referenced throughout
    Sales,
    Inventory,
    Warehouse,
    Shipping,
    Production,
    Accounting,
    CRM,
    Reporting,
    Analytics,
    and Customer Portal modules.
    """

    __tablename__ = "sales_orders"

    order_number: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
        index=True,
        doc="Unique Sales Order number.",
    )

    company_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Reference to the Company.",
    )

    branch_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Reference to the Branch.",
    )

    quotation_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("sales_quotations.id"),
        nullable=True,
        index=True,
        doc="Reference to the originating Sales Quotation.",
    )

    customer_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Reference to the Customer.",
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
        doc="Assigned Approval Workflow.",
    )

    order_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Sales Order date.",
    )

    expected_delivery_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        doc="Expected delivery date.",
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
        doc="Order subtotal before discounts and taxes.",
    )

    discount_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Document discount amount.",
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
        doc="Freight, insurance, packing, and other charges.",
    )

    grand_total: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Final Sales Order amount.",
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="DRAFT",
        doc="Current Sales Order status.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Internal remarks.",
    )

    customer_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Customer-facing notes printed on documents.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether the Sales Order is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------



    quotation: Mapped["SalesQuotation"] = relationship(
        back_populates="sales_orders",
    )


    sales_person: Mapped["SalesPerson"] = relationship(
        back_populates="sales_orders",
    )

    sales_price_list: Mapped["SalesPriceList"] = relationship()

    sales_terms: Mapped["SalesTerms"] = relationship()

    approval_workflow: Mapped["ApprovalWorkflow"] = relationship()

    items: Mapped[list["SalesOrderItem"]] = relationship(
        back_populates="sales_order",
        cascade="all, delete-orphan",
    )