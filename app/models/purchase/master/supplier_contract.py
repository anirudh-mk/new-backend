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
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    pass  # decoupled: from app.models.company.company.company import Company
    pass  # decoupled: from app.models.party.party import Party
    pass  # decoupled: from app.models.core.currency import Currency
    pass  # decoupled: from app.models.accounting.payment_term import PaymentTerm
    from app.models.purchase.purchase_order import PurchaseOrder


class SupplierContract(AuditModel):
    """
    Long-term purchasing agreement with a supplier.

    A supplier contract defines commercial terms that can be
    reused across multiple Purchase Orders.
    """

    __tablename__ = "supplier_contracts"

    company_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
    )

    supplier_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
    )

    contract_no: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    currency_id: Mapped[UUID | None] = mapped_column(
        nullable=True,
    )

    payment_term_id: Mapped[UUID | None] = mapped_column(
        nullable=True,
    )

    contract_value: Mapped[Decimal | None] = mapped_column(
        Numeric(18, 2),
        nullable=True,
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )





    purchase_orders: Mapped[list["PurchaseOrder"]] = relationship(
        back_populates="contract"
    )