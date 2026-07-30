from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    Date,
    ForeignKey,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    pass  # decoupled: from app.models.company.company.company import Company
    pass  # decoupled: from app.models.company.company.branch import Branch
    pass  # decoupled: from app.models.party.party import Party
    from app.models.inventory.warehouse import Warehouse
    from app.models.purchase.purchase_order import PurchaseOrder
    from app.models.purchase.purchase_receipt_item import PurchaseReceiptItem
    from app.models.purchase.landed_cost import LandedCost
    from app.models.purchase.purchase_invoice import PurchaseInvoice
    from app.models.purchase.purchase_receipt_type import PurchaseReceiptType
    pass  # decoupled: from app.models.accounting.journal_status import JournalStatus
    pass  # decoupled: from app.models.user.user import User


class PurchaseReceipt(AuditModel):
    """
    Represents the physical receipt of goods from a supplier.

    Purpose:
        A Purchase Receipt records the actual receipt of goods against a
        Purchase Order. It confirms that ordered items have arrived at
        the warehouse and updates inventory quantities.

        Purchase Receipts may be created as Full Receipt, Partial Receipt,
        Excess Receipt or Replacement Receipt depending on business
        requirements.

        This document becomes the basis for Inventory Updates,
        Landed Cost Allocation and Purchase Invoice verification.

    ERP Workflow:

        Purchase Order
              │
              ▼
        Purchase Receipt
          │        │
          ▼        ▼
      Landed Cost  Purchase Invoice
          │
          ▼
      Inventory Updated

    Business Benefits:
        - Tracks received goods.
        - Supports partial deliveries.
        - Updates inventory.
        - Enables landed cost allocation.
        - Provides supplier delivery history.
        - Supports quality inspection.
        - Creates complete audit trails.

    Relationships:

        PurchaseOrder
            │
            └── PurchaseReceipt

        PurchaseReceipt
            ├── PurchaseReceiptItem
            ├── PurchaseInvoice
            └── LandedCost
    """

    __tablename__ = "purchase_receipts"

    receipt_no: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
        doc="Unique Purchase Receipt number.",
    )

    receipt_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Date on which the goods were received.",
    )

    company_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
    )

    branch_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
    )

    purchase_order_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_orders.id"),
        nullable=False,
        index=True,
    )

    supplier_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
    )

    warehouse_id: Mapped[UUID] = mapped_column(
        ForeignKey("warehouses.id"),
        nullable=False,
        index=True,
    )

    receipt_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_receipt_types.id"),
        nullable=False,
        index=True,
        doc="Type of receipt such as Normal, Partial, Excess or Replacement.",
    )

    received_by: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="User who received the goods.",
    )

    vehicle_no: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        doc="Vehicle number used for delivery.",
    )

    supplier_delivery_note: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        doc="Supplier's delivery challan or delivery note number.",
    )

    inspection_required: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether received goods require quality inspection.",
    )

    remarks: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        doc="Additional remarks regarding the receipt.",
    )

    status_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
    )

    # ----------------------------------------------------------
    # Relationships
    # ----------------------------------------------------------



    purchase_order: Mapped["PurchaseOrder"] = relationship(
        back_populates="receipts",
    )


    warehouse: Mapped["Warehouse"] = relationship()

    receipt_type: Mapped["PurchaseReceiptType"] = relationship()



    items: Mapped[list["PurchaseReceiptItem"]] = relationship(
        back_populates="purchase_receipt",
        cascade="all, delete-orphan",
    )

    landed_costs: Mapped[list["LandedCost"]] = relationship(
        back_populates="purchase_receipt",
    )

    purchase_invoices: Mapped[list["PurchaseInvoice"]] = relationship(
        back_populates="purchase_receipt",
    )