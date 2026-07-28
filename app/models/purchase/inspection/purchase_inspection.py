from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import (
    Date,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.authentication.user import User
    from app.models.company.branch import Branch
    from app.models.company.company import Company
    from app.models.core.journal_status import JournalStatus
    from app.models.purchase.receipt.purchase_receipt import PurchaseReceipt
    from app.models.purchase.inspection.purchase_inspection_item import PurchaseInspectionItem


class PurchaseInspection(BaseModel):
    """
    Represents a quality inspection performed on goods received from a supplier.

    Purpose:
        Purchase Inspection is created after a Purchase Receipt whenever
        received products require quality verification before being
        accepted into inventory.

        Each inspection consists of one or more Purchase Inspection Items,
        where individual products are inspected and accepted or rejected.

    Workflow:

        Purchase Order
                │
                ▼
        Purchase Receipt
                │
                ▼
        Purchase Inspection
                │
                ▼
        Purchase Inspection Item
                │
          ┌─────┴─────┐
          ▼           ▼
      Accepted     Rejected

    Benefits:

        • Quality assurance
        • Acceptance / rejection tracking
        • Supplier quality monitoring
        • Inventory validation
        • Complete inspection audit trail

    Relationships:

        Company
                │
                └── PurchaseInspection

        Branch
                │
                └── PurchaseInspection

        PurchaseReceipt
                │
                └── PurchaseInspection

        User
                │
                └── PurchaseInspection

        JournalStatus
                │
                └── PurchaseInspection

        PurchaseInspectionItem
                │
                └── PurchaseInspection
    """

    __tablename__ = "purchase_inspections"

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
        doc="Company that owns this inspection.",
    )

    branch_id: Mapped[int] = mapped_column(
        ForeignKey("branches.id"),
        nullable=False,
        index=True,
        doc="Branch where the inspection was performed.",
    )

    inspection_no: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
        doc="Unique inspection document number.",
    )

    inspection_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Date of inspection.",
    )

    purchase_receipt_id: Mapped[int] = mapped_column(
        ForeignKey("purchase_receipts.id"),
        nullable=False,
        index=True,
        doc="Reference to the Purchase Receipt.",
    )

    inspected_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
        doc="User who performed the inspection.",
    )

    status_id: Mapped[int] = mapped_column(
        ForeignKey("journal_statuses.id"),
        nullable=False,
        index=True,
        doc="Current inspection status.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional inspection remarks.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    company: Mapped["Company"] = relationship()

    branch: Mapped["Branch"] = relationship()

    purchase_receipt: Mapped["PurchaseReceipt"] = relationship()

    inspector: Mapped["User"] = relationship(
        foreign_keys=[inspected_by],
    )

    status: Mapped["JournalStatus"] = relationship()

    items: Mapped[list["PurchaseInspectionItem"]] = relationship(
        back_populates="purchase_inspection",
        cascade="all, delete-orphan",
    )