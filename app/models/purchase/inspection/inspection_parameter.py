from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.company.company.company import Company


class InspectionParameter(AuditModel):
    """
    Master table representing quality inspection parameters (e.g. Length, Weight, Hardness).
    """

    __tablename__ = "inspection_parameters"

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
    )

    code: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
        doc="Unique code identifying the inspection parameter.",
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="Name of the parameter (e.g. Hardness, Outer Diameter).",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Relationships
    company: Mapped["Company"] = relationship()

    def __repr__(self) -> str:
        return f"<InspectionParameter(code='{self.code}', name='{self.name}')>"
