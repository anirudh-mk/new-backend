from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.user.user import User
    from app.models.company.company.company import Company
    from app.models.purchase.order.purchase_order import PurchaseOrder


class PurchaseTerms(BaseModel):
    """
    Master table for Purchase Terms & Conditions.

    Examples:
        - Payment within 30 days.
        - Goods once sold cannot be returned.
        - Warranty for 24 months.
        - Delivery at buyer warehouse.
        - Installation included.

    A Purchase Order references this table instead of storing
    the same text repeatedly.
    """

    __tablename__ = "purchase_terms"

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
    )

    code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_by_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    updated_by_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Relationships
    company: Mapped["Company"] = relationship()

    created_by: Mapped["User"] = relationship(
        foreign_keys=[created_by_id]
    )

    updated_by: Mapped["User"] = relationship(
        foreign_keys=[updated_by_id]
    )

    purchase_orders: Mapped[list["PurchaseOrder"]] = relationship(
        back_populates="terms"
    )

    def __repr__(self) -> str:
        return f"<PurchaseTerms(code='{self.code}', name='{self.name}')>"