from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    Numeric,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.accounting.charge_type import ChargeType
    from app.models.purchase.returns.purchase_return import PurchaseReturn


class PurchaseReturnCharge(BaseModel):
    """
    Represents an additional charge/deduction applied to a Purchase Return.
    """

    __tablename__ = "purchase_return_charges"

    purchase_return_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_returns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Reference to the Purchase Return.",
    )

    charge_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("charge_types.id"),
        nullable=False,
        index=True,
        doc="Type of additional charge.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional description of the charge.",
    )

    amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Charge amount before tax.",
    )

    tax_percentage: Mapped[float] = mapped_column(
        Numeric(8, 2),
        nullable=False,
        default=0,
        doc="Tax percentage applied to the charge.",
    )

    tax_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Calculated tax amount.",
    )

    line_total: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Net charge amount including tax.",
    )

    line_no: Mapped[int] = mapped_column(
        nullable=False,
    )

    # Relationships
    purchase_return: Mapped["PurchaseReturn"] = relationship(back_populates="charges")
    charge_type: Mapped["ChargeType"] = relationship()

    def __repr__(self) -> str:
        return f"<PurchaseReturnCharge(return_id='{self.purchase_return_id}', total={self.line_total})>"
