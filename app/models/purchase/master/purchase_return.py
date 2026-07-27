from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Date,
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.company.company import Company
    from app.models.company.branch import Branch
    from app.models.party.party import Party
    from app.models.inventory.warehouse import Warehouse
    from app.models.purchase.purchase_order import PurchaseOrder
    from app.models.purchase.purchase_receipt import PurchaseReceipt
    from app.models.purchase.purchase_invoice import PurchaseInvoice
    from app.models.purchase.purchase_return_item import PurchaseReturnItem
    from app.models.purchase.purchase_return_type import PurchaseReturnType
    from app.models.accounting.journal_status import JournalStatus


class PurchaseReturn(AuditModel):
    """
    Represents goods returned to a supplier.

    Purpose:
        A Purchase Return records the return of purchased goods to a
        supplier due to defects, damage, expiry, incorrect delivery,
        excess quantity, or other business reasons.

        The document reduces inventory quantities and may generate a
        supplier credit note or reduce the outstanding Accounts Payable.

    Workflow:

        Purchase Order
              │
              ▼
        Purchase Receipt
              │
              ▼
        Purchase Invoice
              │
              ▼
        Purchase Return
              │
              ▼
        Supplier Credit / AP Adjustment

    Business Benefits:
        - Records returned goods.
        - Maintains inventory accuracy.
        - Reduces supplier payable.
        - Supports supplier credit notes.
        - Provides complete audit trail.
        - Supports quality and warranty claims.
        - Tracks return reasons.

    Relationships:

        PurchaseReturn
            ├── PurchaseReturnItem
            ├── PurchaseReceipt
            ├── PurchaseInvoice
            └── PurchaseOrder
    """

    __tablename__ = "purchase_returns"

    return_no: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
        doc="Unique Purchase Return number.",
    )

    return_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Date of supplier return.",
    )

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
    )

    branch_id: Mapped[int] = mapped_column(
        ForeignKey("branches.id"),
        nullable=False,
        index=True,
    )

    purchase_order_id: Mapped[int | None] = mapped_column(
        ForeignKey("purchase_orders.id"),
        nullable=True,
        index=True,
    )

    purchase_receipt_id: Mapped[int] = mapped_column(
        ForeignKey("purchase_receipts.id"),
        nullable=False,
        index=True,
    )

    purchase_invoice_id: Mapped[int | None] = mapped_column(
        ForeignKey("purchase_invoices.id"),
        nullable=True,
        index=True,
    )

    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("parties.id"),
        nullable=False,
        index=True,
    )

    warehouse_id: Mapped[int | None] = mapped_column(
        ForeignKey("warehouses.id"),
        nullable=True,
        index=True,
    )

    return_type_id: Mapped[int] = mapped_column(
        ForeignKey("purchase_return_types.id"),
        nullable=False,
        index=True,
        doc="Type of supplier return.",
    )

    reason: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        doc="Reason for returning the goods.",
    )

    subtotal: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
    )

    discount_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
    )

    tax_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
    )

    other_charges: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
    )

    grand_total: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
    )

    remarks: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    status_id: Mapped[int] = mapped_column(
        ForeignKey("journal_statuses.id"),
        nullable=False,
        index=True,
    )

    is_posted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    is_cancelled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    company: Mapped["Company"] = relationship()

    branch: Mapped["Branch"] = relationship()

    supplier: Mapped["Party"] = relationship()

    purchase_order: Mapped["PurchaseOrder"] = relationship()

    purchase_receipt: Mapped["PurchaseReceipt"] = relationship()

    purchase_invoice: Mapped["PurchaseInvoice"] = relationship()

    warehouse: Mapped["Warehouse"] = relationship()

    return_type: Mapped["PurchaseReturnType"] = relationship()

    status: Mapped["JournalStatus"] = relationship()

    items: Mapped[list["PurchaseReturnItem"]] = relationship(
        back_populates="purchase_return",
        cascade="all, delete-orphan",
    )
