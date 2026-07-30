from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.purchase.master.landed_cost import LandedCost


class LandedCostCharge(BaseModel):
    """
    Represents individual expense breakdown items for Landed Costs (e.g. Freight, Port, Customs).
    """

    __tablename__ = "landed_cost_charges"

    landed_cost_id: Mapped[UUID] = mapped_column(
        ForeignKey("landed_costs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    charge_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="Type of charge (e.g. Freight, Customs Duty, Insurance, Port Charges).",
    )

    amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Amount of the charge.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Relationships
    landed_cost: Mapped["LandedCost"] = relationship(back_populates="charges")

    def __repr__(self) -> str:
        return f"<LandedCostCharge(landed_cost_id='{self.landed_cost_id}', type='{self.charge_type}', amount={self.amount})>"