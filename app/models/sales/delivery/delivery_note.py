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
    from app.models.sales.order.sales_order import SalesOrder
    from app.models.sales.master.sales_person import SalesPerson
    from app.models.workflow.approval_workflow import ApprovalWorkflow
    from app.models.sales.delivery.delivery_note_item import DeliveryNoteItem


class DeliveryNote(BaseModel):
    """
    Represents a Delivery Note issued for a Sales Order.

    Purpose:
        A Delivery Note is the official document used to
        record the physical delivery of products to a customer.

        It acts as proof that goods have been dispatched
        from the warehouse and delivered to the customer.

        A Delivery Note is generated after a Sales Order
        has been approved and inventory has been allocated.

        One Sales Order may generate one or more Delivery Notes,
        allowing support for partial deliveries.

    Examples:

        Sales Order

            SO-2026-00125

        Delivery 1

            DN-2026-00045

            50 Products Delivered

        Delivery 2

            DN-2026-00048

            Remaining 25 Products Delivered

    Workflow:

            Sales Order
                 │
                 ▼
         Inventory Reservation
                 │
                 ▼
            Delivery Note
                 │
                 ▼
          Warehouse Picking
                 │
                 ▼
              Shipment
                 │
                 ▼
          Customer Receipt
                 │
                 ▼
            Sales Invoice

    Benefits:

        • Supports partial deliveries.
        • Inventory deduction.
        • Warehouse integration.
        • Shipment tracking.
        • Customer acknowledgment.
        • Invoice generation.
        • Complete delivery history.
        • Batch tracking.
        • Serial number tracking.
        • Logistics integration.

    Relationships:

                Company
                   │
                   ▼
             DeliveryNote
        ┌──────────┼──────────┬───────────┐
        ▼          ▼          ▼           ▼
    Customer   SalesOrder Warehouse SalesPerson
                   │
                   ▼
          DeliveryNoteItem

    Example:

        Delivery No

            DN-2026-000123

        Customer

            ABC Super Market

        Warehouse

            Main Warehouse

        Status

            Delivered

    Notes:

        • One Sales Order may have multiple Delivery Notes.
        • One Delivery Note contains multiple items.
        • Inventory is reduced upon confirmation.
        • Delivery can be partial or complete.
        • Supports warehouse operations.
        • Supports logistics integration.
        • Supports proof of delivery.
        • Historical records should never be modified.

    This model is referenced throughout
    Sales,
    Inventory,
    Warehouse,
    Logistics,
    Shipping,
    Customer Service,
    Accounting,
    Reporting,
    Analytics,
    and Supply Chain modules.
    """

    __tablename__ = "delivery_notes"

    delivery_number: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
        index=True,
        doc="Unique Delivery Note number.",
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

    sales_order_id: Mapped[UUID] = mapped_column(
        ForeignKey("sales_orders.id"),
        nullable=False,
        index=True,
        doc="Reference to the Sales Order.",
    )

    customer_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Reference to the Customer.",
    )

    warehouse_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Warehouse responsible for the delivery.",
    )

    sales_person_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("sales_persons.id"),
        nullable=True,
        index=True,
        doc="Sales Person associated with this delivery.",
    )

    approval_workflow_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("approval_workflows.id"),
        nullable=True,
        index=True,
        doc="Approval Workflow used for this Delivery Note.",
    )

    delivery_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Actual delivery date.",
    )

    expected_delivery_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        doc="Expected delivery date.",
    )

    vehicle_number: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
        doc="Vehicle used for delivery.",
    )

    driver_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        doc="Driver responsible for delivery.",
    )

    tracking_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
        doc="Courier or logistics tracking number.",
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Total value before taxes and charges.",
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
        doc="Freight, insurance and additional charges.",
    )

    grand_total: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Final delivery value.",
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="DRAFT",
        doc="Current Delivery Note status.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Internal remarks.",
    )

    customer_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Customer-facing notes.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether this Delivery Note is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------



    sales_order: Mapped["SalesOrder"] = relationship(
        back_populates="delivery_notes",
    )



    sales_person: Mapped["SalesPerson"] = relationship(
        back_populates="delivery_notes",
    )

    approval_workflow: Mapped["ApprovalWorkflow"] = relationship()

    items: Mapped[list["DeliveryNoteItem"]] = relationship(
        back_populates="delivery_note",
        cascade="all, delete-orphan",
    )