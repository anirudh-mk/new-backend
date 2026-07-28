from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Date,
    ForeignKey,
    Numeric,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.company.company.company import Company
    from app.models.party.party import Party


class SupplierPerformance(BaseModel):
    """
    Stores calculated or evaluated supplier performance metrics for analytics.
    """

    __tablename__ = "supplier_performances"

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
    )

    supplier_id: Mapped[UUID] = mapped_column(
        ForeignKey("parties.id"),
        nullable=False,
        index=True,
    )

    evaluation_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Date on which metrics were calculated or recorded.",
    )

    on_time_delivery_rate: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=100.00,
        doc="Percentage of orders delivered on or before expected date.",
    )

    average_delay_days: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=0.00,
        doc="Average delay in days for late shipments.",
    )

    quality_rate: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=100.00,
        doc="Percentage of items accepted after quality inspection.",
    )

    return_rate: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=0.00,
        doc="Percentage of items returned back to the supplier.",
    )

    price_rating: Mapped[float] = mapped_column(
        Numeric(3, 2),
        nullable=False,
        default=5.00,
        doc="Supplier price rating (e.g. scale of 1 to 5).",
    )

    overall_score: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=100.00,
        doc="Aggregated performance score.",
    )

    # Relationships
    company: Mapped["Company"] = relationship()
    supplier: Mapped["Party"] = relationship()

    def __repr__(self) -> str:
        return f"<SupplierPerformance(supplier_id='{self.supplier_id}', score={self.overall_score})>"
