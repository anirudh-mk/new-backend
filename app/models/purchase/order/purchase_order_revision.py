from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.purchase.order.purchase_order import PurchaseOrder
    from app.models.user.user import User


class PurchaseOrderRevision(BaseModel):
    """
    Stores complete historical snapshots of a Purchase Order when revised.
    """

    __tablename__ = "purchase_order_revisions"

    purchase_order_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Reference to the Purchase Order.",
    )

    revision_no: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        doc="Revision number.",
    )

    revised_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        doc="Timestamp of the revision.",
    )

    revised_by_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
        doc="User who revised the order.",
    )

    change_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Brief summary explaining what was modified.",
    )

    snapshot: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        doc="Complete JSON dump of the Purchase Order state, items, taxes, charges.",
    )

    # Relationships
    purchase_order: Mapped["PurchaseOrder"] = relationship(back_populates="revisions")
    revised_by: Mapped["User"] = relationship(foreign_keys=[revised_by_id])

    def __repr__(self) -> str:
        return f"<PurchaseOrderRevision(purchase_order_id='{self.purchase_order_id}', rev={self.revision_no})>"
