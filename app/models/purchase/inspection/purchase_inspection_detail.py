from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.purchase.inspection.purchase_inspection_item import PurchaseInspectionItem
    from app.models.purchase.inspection.inspection_parameter import InspectionParameter


class PurchaseInspectionDetail(BaseModel):
    """
    Records specific measured parameters and checks for inspected receipt items.
    """

    __tablename__ = "purchase_inspection_details"

    purchase_inspection_item_id: Mapped[UUID] = mapped_column(
        ForeignKey("purchase_inspection_items.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    parameter_id: Mapped[UUID] = mapped_column(
        ForeignKey("inspection_parameters.id"),
        nullable=False,
        index=True,
    )

    observed_value: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="Measured value recorded during inspection.",
    )

    result: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        doc="Outcome (e.g. Pass, Fail).",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Relationships
    purchase_inspection_item: Mapped["PurchaseInspectionItem"] = relationship(back_populates="inspection_details")
    parameter: Mapped["InspectionParameter"] = relationship()

    def __repr__(self) -> str:
        return f"<PurchaseInspectionDetail(item_id='{self.purchase_inspection_item_id}', result='{self.result}')>"
