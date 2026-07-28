from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel, BaseModel

if TYPE_CHECKING:
    from app.models.company.company import Company
    from app.models.user.user import User


class ApprovalWorkflow(AuditModel):
    """
    Represents a configurable approval routing rule based on transaction limits.
    """

    __tablename__ = "approval_workflows"

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="Name of the workflow ruleset.",
    )

    document_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="Document type this workflow applies to (e.g. PurchaseRequisition, PurchaseOrder).",
    )

    min_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Minimum amount required to trigger this workflow.",
    )

    max_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=9999999999.99,
        doc="Maximum amount up to which this workflow applies.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Relationships
    company: Mapped["Company"] = relationship()
    
    steps: Mapped[list["ApprovalWorkflowStep"]] = relationship(
        back_populates="workflow",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<ApprovalWorkflow(name='{self.name}', doc_type='{self.document_type}')>"


class ApprovalWorkflowStep(BaseModel):
    """
    Represents a specific approval level/step in an approval workflow.
    """

    __tablename__ = "approval_workflow_steps"

    workflow_id: Mapped[UUID] = mapped_column(
        ForeignKey("approval_workflows.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        doc="Workflow level order (e.g. 1, 2, 3).",
    )

    role_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True,
        doc="Optional role required to approve at this step.",
    )

    department_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True,
        doc="Optional department required to approve at this step.",
    )

    user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True,
        doc="Specific user required to approve at this step.",
    )

    approver_label: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="Descriptive label (e.g. Department Manager, Finance Head, CEO).",
    )

    # Relationships
    workflow: Mapped["ApprovalWorkflow"] = relationship(back_populates="steps")
    user: Mapped["User"] = relationship()

    def __repr__(self) -> str:
        return f"<ApprovalWorkflowStep(level={self.level}, label='{self.approver_label}')>"
