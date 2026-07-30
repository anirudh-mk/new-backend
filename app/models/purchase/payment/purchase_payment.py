from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Date,
    ForeignKey,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    pass  # decoupled: from app.models.accounting.bank_account import BankAccount
    pass  # decoupled: from app.models.core.currency import Currency
    pass  # decoupled: from app.models.user.user import User
    pass  # decoupled: from app.models.company.company.branch import Branch
    pass  # decoupled: from app.models.company.company.company import Company
    pass  # decoupled: from app.models.party.party import Party
    from app.models.finance.payment_method import PaymentMethod
    pass  # decoupled: from app.models.accounting.journal_status import JournalStatus
    from app.models.purchase.payment.purchase_payment_allocation import PurchasePaymentAllocation


class PurchasePayment(BaseModel):
    """
    Represents a standalone supplier payment that can be allocated to multiple invoices.
    """

    __tablename__ = "purchase_payments"

    company_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Company that owns this payment.",
    )

    branch_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Branch that owns this payment.",
    )

    supplier_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Supplier/party receiving the payment.",
    )

    payment_no: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
        doc="Unique payment reference number.",
    )

    payment_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Date on which the payment was made.",
    )

    payment_method_id: Mapped[UUID] = mapped_column(
        ForeignKey("payment_methods.id"),
        nullable=False,
        index=True,
        doc="Payment method used.",
    )

    currency_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Payment currency.",
    )

    exchange_rate: Mapped[float] = mapped_column(
        Numeric(18, 6),
        nullable=False,
        default=1,
        doc="Exchange rate applied to the payment.",
    )

    paid_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Total amount paid to the supplier.",
    )

    bank_account_id: Mapped[UUID | None] = mapped_column(
        nullable=True,
        index=True,
        doc="Bank account used for the payment.",
    )

    reference_no: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        doc="Payment transaction reference, cheque number, UTR, etc.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional remarks.",
    )

    status_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
    )

    # Relationships
    payment_method: Mapped["PaymentMethod"] = relationship()

    allocations: Mapped[list["PurchasePaymentAllocation"]] = relationship(
        back_populates="payment",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<PurchasePayment(payment_no='{self.payment_no}', paid_amount={self.paid_amount})>"