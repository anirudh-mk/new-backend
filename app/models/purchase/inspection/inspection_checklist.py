from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel, BaseModel

if TYPE_CHECKING:
    pass  # decoupled: from app.models.company.company.company import Company
    from app.models.inventory.product.product import Product
    from app.models.purchase.inspection.inspection_parameter import InspectionParameter


class InspectionChecklist(AuditModel):
    """
    Template checklist linking a collection of parameters to products.
    """

    __tablename__ = "inspection_checklists"

    company_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="Name of the checklist.",
    )

    product_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("products.id"),
        nullable=True,
        index=True,
        doc="Product this checklist template is designed for (optional, can be general).",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Relationships
    product: Mapped["Product"] = relationship()

    parameters: Mapped[list["InspectionChecklistParameter"]] = relationship(
        back_populates="checklist",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<InspectionChecklist(name='{self.name}', product_id='{self.product_id}')>"


class InspectionChecklistParameter(BaseModel):
    """
    Links an inspection parameter to a checklist template with limits.
    """

    __tablename__ = "inspection_checklist_parameters"

    checklist_id: Mapped[UUID] = mapped_column(
        ForeignKey("inspection_checklists.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    parameter_id: Mapped[UUID] = mapped_column(
        ForeignKey("inspection_parameters.id"),
        nullable=False,
        index=True,
    )

    spec_value: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="Expected standard specification value (e.g. 10m, 60 HRC).",
    )

    min_tolerance: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        doc="Minimum acceptable deviation.",
    )

    max_tolerance: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        doc="Maximum acceptable deviation.",
    )

    is_mandatory: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        doc="Indicates if failure on this parameter rejects the entire item.",
    )

    # Relationships
    checklist: Mapped["InspectionChecklist"] = relationship(back_populates="parameters")
    parameter: Mapped["InspectionParameter"] = relationship()

    def __repr__(self) -> str:
        return f"<InspectionChecklistParameter(checklist_id='{self.checklist_id}', parameter_id='{self.parameter_id}')>"