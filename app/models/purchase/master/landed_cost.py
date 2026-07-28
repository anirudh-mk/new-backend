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
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.company.company import Company
    from app.models.compan.branch import Branch
    from app.models.core.currency import Currency
    from app.models.purchase.purchase_receipt import PurchaseReceipt
    from app.models.purchase.landed_cost_item import LandedCostItem
    from app.models.purchase.landed_cost_allocation_method import (
        LandedCostAllocationMethod,
    )
    from app.models.accounting.journal_status import JournalStatus


class LandedCost(AuditModel):
    """
    Represents additional costs incurred to bring purchased goods
    into inventory.

    Purpose:
        Landed Cost records expenses incurred after purchasing goods
        but before they are available for sale or use. Examples include
        freight, customs duty, insurance, port charges, transportation,
        loading/unloading, clearing charges, and handling fees.

        These costs are allocated to inventory items so that the actual
        inventory valuation reflects the true acquisition cost.

    Workflow:

        Purchase Order
              │
              ▼
        Purchase Receipt
              │
              ▼
          Landed Cost
              │
              ▼
        Cost Allocation
              │
              ▼
        Inventory Valuation Updated

    Business Benefits:
        - Accurate inventory valuation.
        - Supports import purchasing.
        - Allocates freight and customs.
        - Improves profit calculations.
        - Complies with accounting standards.
        - Supports multiple allocation methods.
        - Provides complete audit history.

    Relationships:

        PurchaseReceipt
            └── LandedCost

        LandedCost
            ├── LandedCostItem
            └── AllocationMethod
    """

    __tablename__ = "landed_costs"

    landed_cost_no: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
        doc="Unique Landed Cost document number.",
    )

    landed_cost_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Date the landed cost document was created.",
    )

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
    )

    branch_id: Mapped[UUID] = mapped_column(
        ForeignKey("branches.id"),
        nullable=False,
        index=True,
    )

    purchase_receipt_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_receipts.id"),
        nullable=False,
        index=True,
        doc="Purchase Receipt to which the landed cost applies.",
    )

    currency_id: Mapped[UUID] = mapped_column(
        ForeignKey("currencies.id"),
        nullable=False,
        index=True,
    )

    exchange_rate: Mapped[float] = mapped_column(
        Numeric(18, 6),
        nullable=False,
        default=1,
        doc="Exchange rate for the selected currency.",
    )

    total_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Total landed cost amount to be allocated.",
    )

    allocation_method_id: Mapped[UUID] = mapped_column(
        ForeignKey("landed_cost_allocation_methods.id"),
        nullable=False,
        index=True,
        doc="Method used to distribute landed cost among items.",
    )

    remarks: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        doc="Additional remarks.",
    )

    status_id: Mapped[UUID] = mapped_column(
        ForeignKey("journal_statuses.id"),
        nullable=False,
        index=True,
    )

    is_applied: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether the landed cost has been applied to inventory.",
    )

    is_cancelled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether the landed cost document is cancelled.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    company: Mapped["Company"] = relationship()

    branch: Mapped["Branch"] = relationship()

    purchase_receipt: Mapped["PurchaseReceipt"] = relationship(
        back_populates="landed_costs",
    )

    currency: Mapped["Currency"] = relationship()

    allocation_method: Mapped["LandedCostAllocationMethod"] = relationship()

    status: Mapped["JournalStatus"] = relationship()

    items: Mapped[list["LandedCostItem"]] = relationship(
        back_populates="landed_cost",
        cascade="all, delete-orphan",
    )

    charges: Mapped[list["LandedCostCharge"]] = relationship(
        back_populates="landed_cost",
        cascade="all, delete-orphan",
    )