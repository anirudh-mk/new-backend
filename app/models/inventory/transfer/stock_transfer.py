from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    DateTime,
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
    from app.models.company.branch import Branch
    from app.models.company.company import Company
    from app.models.inventory.transfer.stock_transfer_item import StockTransferItem
    from app.models.inventory.warehouse.warehouse import Warehouse
    from app.models.users.user import User


class StockTransfer(BaseModel):
    """
    Represents an inventory transfer document between Warehouses.

    Purpose:
        Stock Transfer moves inventory from one Warehouse to another
        without affecting overall company inventory.

        Transfers support movement between:

            • Warehouse → Warehouse
            • Branch → Branch
            • Warehouse Locations
            • Transit Warehouses

        A transfer consists of a document header and one or more
        Stock Transfer Items.

        Posting the transfer creates corresponding StockTransaction
        records:

            Source Warehouse

                OUT

            Destination Warehouse

                IN

    Workflow:

            Stock Transfer
                    │
                    ▼
                Approval
                    │
                    ▼
                Dispatch
                    │
                    ▼
                In Transit
                    │
                    ▼
                 Receiving
                    │
                    ▼
            Stock Transactions

    Benefits:

        • Warehouse-to-Warehouse transfers.
        • Branch transfers.
        • Complete audit trail.
        • Multi-stage workflow.
        • Batch tracking.
        • Serial tracking.
        • In-transit inventory.
        • Warehouse balancing.

    Relationships:

            Company
                │
                ▼
             Branch
                │
                ▼
         Stock Transfer
                │
                ▼
       Stock Transfer Items

    Notes:

        • One document may contain multiple products.
        • Posting generates StockTransaction entries.
        • Source warehouse decreases inventory.
        • Destination warehouse increases inventory.
        • Posted transfers should never be modified.

    Referenced throughout Inventory,
    Warehouse,
    Logistics,
    Manufacturing,
    Purchase,
    Sales,
    and Reporting modules.
    """

    __tablename__ = "stock_transfers"

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
        doc="Company initiating the transfer.",
    )

    branch_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("branches.id"),
        nullable=True,
        index=True,
        doc="Branch initiating the transfer.",
    )

    transfer_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
        doc="Unique transfer document number.",
    )

    transfer_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        doc="Transfer document date.",
    )

    from_warehouse_id: Mapped[UUID] = mapped_column(
        ForeignKey("warehouses.id"),
        nullable=False,
        index=True,
        doc="Source warehouse.",
    )

    to_warehouse_id: Mapped[UUID] = mapped_column(
        ForeignKey("warehouses.id"),
        nullable=False,
        index=True,
        doc="Destination warehouse.",
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="DRAFT",
        index=True,
        doc="Current workflow status.",
    )

    reference_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        doc="External reference number.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional transfer remarks.",
    )

    approved_by_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True,
        doc="User approving the transfer.",
    )

    approved_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        doc="Approval timestamp.",
    )

    dispatched_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        doc="Dispatch timestamp.",
    )

    received_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        doc="Receiving timestamp.",
    )

    is_posted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether inventory has been updated.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    company: Mapped["Company"] = relationship()

    branch: Mapped["Branch | None"] = relationship()

    from_warehouse: Mapped["Warehouse"] = relationship(
        foreign_keys=[from_warehouse_id],
        back_populates="stock_transfers_from",
    )

    to_warehouse: Mapped["Warehouse"] = relationship(
        foreign_keys=[to_warehouse_id],
        back_populates="stock_transfers_to",
    )

    approved_by: Mapped["User | None"] = relationship()

    items: Mapped[list["StockTransferItem"]] = relationship(
        back_populates="stock_transfer",
        cascade="all, delete-orphan",
    )