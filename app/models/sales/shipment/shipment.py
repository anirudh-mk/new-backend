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
    from app.models.company.company import Company
    from app.models.company.branch import Branch
    from app.models.party.customer.customer import Customer
    from app.models.sales.order.sales_order import SalesOrder
    from app.models.sales.delivery.delivery_note import DeliveryNote
    from app.models.sales.master.sales_person import SalesPerson
    from app.models.workflow.approval_workflow import ApprovalWorkflow
    from app.models.sales.shipment.shipment_item import ShipmentItem


class Shipment(BaseModel):
    """
    Represents a Shipment created for delivering goods to a customer.

    Purpose:
        Shipment represents the physical transportation of
        goods from a warehouse to the customer's delivery
        location.

        It acts as the logistics document between the
        Delivery Note and the actual delivery.

        A Shipment may contain products from one or
        multiple Delivery Notes depending on the
        organization's logistics process.

        The Shipment tracks vehicle information,
        driver details, courier information,
        shipment status, dispatch date,
        estimated delivery, and delivery confirmation.

    Examples:

        Shipment Number

            SHP-2026-000125

        Customer

            ABC Super Market

        Vehicle

            KL-11-AA-4587

        Courier

            Blue Dart

    Workflow:

            Sales Order
                  │
                  ▼
            Delivery Note
                  │
                  ▼
              Shipment
                  │
        ┌─────────┼──────────┐
        ▼         ▼          ▼
    Dispatch   In Transit  Delivered
                  │
                  ▼
           Customer Receipt

    Benefits:

        • Shipment tracking.
        • Vehicle management.
        • Driver assignment.
        • Courier integration.
        • Multiple shipment support.
        • Partial shipment support.
        • Delivery confirmation.
        • Complete logistics history.
        • Customer tracking.
        • Audit trail.

    Relationships:

              Company
                 │
                 ▼
             Shipment
      ┌────────┼────────┬─────────┬──────────┐
      ▼        ▼        ▼         ▼
 Customer  SalesOrder DeliveryNote ShipmentItems

    Example:

        Shipment

            SHP-2026-000125

        Driver

            Ramesh Kumar

        Vehicle

            KL-11-AA-4587

        Status

            IN_TRANSIT

    Notes:

        • One Shipment contains multiple items.
        • One Delivery Note may have multiple shipments.
        • Supports partial deliveries.
        • Supports multiple warehouses.
        • Supports third-party logistics.
        • Supports proof of delivery.
        • Historical records should never change.

    Referenced throughout
    Sales,
    Logistics,
    Warehouse,
    Inventory,
    Customer Portal,
    Fleet Management,
    Finance,
    Reporting,
    Analytics,
    and Compliance modules.
    """

    __tablename__ = "shipments"

    shipment_number: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
        doc="Unique Shipment number.",
    )

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
        doc="Reference to the Company.",
    )

    branch_id: Mapped[UUID] = mapped_column(
        ForeignKey("branches.id"),
        nullable=False,
        index=True,
        doc="Reference to the Branch.",
    )

    sales_order_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("sales_orders.id"),
        nullable=True,
        index=True,
        doc="Reference to the originating Sales Order.",
    )

    delivery_note_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("delivery_notes.id"),
        nullable=True,
        index=True,
        doc="Reference to the Delivery Note.",
    )

    customer_id: Mapped[UUID] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
        index=True,
        doc="Reference to the Customer.",
    )

    sales_person_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("sales_persons.id"),
        nullable=True,
        index=True,
        doc="Sales Person responsible for the shipment.",
    )

    approval_workflow_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("approval_workflows.id"),
        nullable=True,
        index=True,
        doc="Approval workflow associated with the shipment.",
    )

    shipment_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Shipment creation date.",
    )

    expected_delivery_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        doc="Expected delivery date.",
    )

    carrier_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        doc="Courier or logistics company.",
    )

    tracking_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
        doc="Courier tracking number.",
    )

    vehicle_number: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
        doc="Vehicle registration number.",
    )

    driver_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        doc="Assigned driver's name.",
    )

    shipping_cost: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Shipping cost.",
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="DRAFT",
        doc="Shipment status.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Internal shipment remarks.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether the shipment is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    company: Mapped["Company"] = relationship(
        back_populates="shipments",
    )

    branch: Mapped["Branch"] = relationship(
        back_populates="shipments",
    )

    sales_order: Mapped["SalesOrder"] = relationship(
        back_populates="shipments",
    )

    delivery_note: Mapped["DeliveryNote"] = relationship(
        back_populates="shipments",
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="shipments",
    )

    sales_person: Mapped["SalesPerson"] = relationship(
        back_populates="shipments",
    )

    approval_workflow: Mapped["ApprovalWorkflow"] = relationship()

    items: Mapped[list["ShipmentItem"]] = relationship(
        back_populates="shipment",
        cascade="all, delete-orphan",
    )