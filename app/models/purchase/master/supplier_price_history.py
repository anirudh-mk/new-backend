from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Numeric,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.purchase.master.supplier_price import SupplierPrice
    from app.models.user.user import User


class SupplierPriceHistory(BaseModel):
    """
    Represents historical records of pricing updates for supplier-specific product prices.
    """

    __tablename__ = "supplier_price_histories"

    supplier_price_id: Mapped[UUID] = mapped_column(
        ForeignKey("supplier_prices.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Reference to the current Supplier Price master record.",
    )

    price: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="The supplier price before this change.",
    )

    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        doc="Timestamp when the price was changed.",
    )

    changed_by_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
        doc="User who updated the price.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Change explanation or comments.",
    )

    # Relationships
    supplier_price: Mapped["SupplierPrice"] = relationship(back_populates="history")
    changed_by: Mapped["User"] = relationship(foreign_keys=[changed_by_id])

    def __repr__(self) -> str:
        return f"<SupplierPriceHistory(supplier_price_id='{self.supplier_price_id}', price={self.price}, changed_at='{self.changed_at}')>"
