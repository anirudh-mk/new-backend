from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.company.company import Company
    from app.models.company.branch import Branch
    from app.models.accounting.ledger import Ledger


class BudgetReservation(AuditModel):
    """
    Tracks budget allocations and reservations for purchase transactions.
    """

    __tablename__ = "budget_reservations"

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

    department_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True,
        index=True,
        doc="Optional department holding the budget.",
    )

    account_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("ledgers.id"),
        nullable=True,
        index=True,
        doc="Budget ledger account.",
    )

    document_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="Document type creating the reservation (e.g. PurchaseRequisition, PurchaseOrder).",
    )

    document_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        index=True,
        doc="Primary key UUID of the document.",
    )

    fiscal_year: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        doc="Fiscal year of the budget (e.g. 2026-27).",
    )

    period: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
        doc="Budget period (e.g. Q1, January).",
    )

    budget_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Total budget allocated for the account and period.",
    )

    reserved_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Amount blocked/reserved by this transaction.",
    )

    utilized_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Amount successfully utilized/converted to actual invoice.",
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="Active",
        doc="Reservation status (e.g. Active, Released, Cancelled).",
    )

    # Relationships
    company: Mapped["Company"] = relationship()
    branch: Mapped["Branch"] = relationship()
    account: Mapped["Ledger"] = relationship()

    def __repr__(self) -> str:
        return f"<BudgetReservation(doc_type='{self.document_type}', reserved={self.reserved_amount}, status='{self.status}')>"
