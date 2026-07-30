from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.company.company import Company
    from app.models.workflow.approval_workflow_step import ApprovalWorkflowStep


class ApprovalWorkflow(BaseModel):
    """
    Represents a reusable Approval Workflow Definition.

    Purpose:
        Approval Workflow defines the approval process that business
        documents must follow before they become effective.

        Instead of hardcoding approval logic into individual modules,
        Approval Workflow provides a configurable approval engine
        that can be reused throughout the ERP.

        A workflow consists of one or more Approval Steps.
        Each step specifies who must approve the document,
        the approval sequence, and any approval conditions.

        Business documents such as Purchase Orders,
        Sales Orders, Journal Entries, Expense Claims,
        Inventory Adjustments, and Leave Requests
        may all reference an Approval Workflow.

    Examples:

        Purchase Order Workflow

            Level 1
                Purchase Executive

            Level 2
                Purchase Manager

            Level 3
                Finance Manager

        Sales Discount Workflow

            Sales Manager
                    ↓
            General Manager

        Expense Approval

            Department Head
                    ↓
            Finance

        Leave Approval

            Team Lead
                    ↓
            HR Manager

    Workflow:

                    Company
                       │
                       ▼
              Approval Workflow
                       │
                       ▼
            Approval Workflow Steps
                       │
                       ▼
               Business Document
                       │
                       ▼
              Approval History

    Benefits:

        • Reusable across ERP modules.
        • Unlimited approval levels.
        • Sequential approvals.
        • Parallel approvals.
        • Conditional approvals.
        • Delegation support.
        • Approval history.
        • Email notifications.
        • Mobile approvals.
        • Complete audit trail.

    Relationships:

                    Company
                       │
                       ▼
              Approval Workflow
                       │
                       ▼
            Approval Workflow Step

    Example:

        Workflow

            Purchase Order Approval

        Module

            Purchase

        Document

            Purchase Order

        Levels

            Purchase Manager
            Finance Manager
            Director

    Notes:

        • Workflows are reusable.
        • Multiple workflows may exist for one module.
        • Workflows may be activated/deactivated.
        • Steps are maintained separately.
        • Approval history is stored separately.
        • Supports unlimited approval levels.
        • Supports amount-based routing.
        • Supports role-based approvals.

    This model is referenced throughout
    Purchase,
    Sales,
    Inventory,
    Manufacturing,
    Accounting,
    Finance,
    HR,
    CRM,
    Asset Management,
    Payroll,
    and Reporting modules.
    """

    __tablename__ = "approval_workflows"

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
        doc="Reference to the Company.",
    )

    code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
        index=True,
        doc="Unique Approval Workflow code.",
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
        doc="Display name of the Approval Workflow.",
    )

    module: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="ERP module to which this workflow belongs.",
    )

    document_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        doc="Document type using this Approval Workflow.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Description of the workflow.",
    )

    priority: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
        doc="Priority used when multiple workflows are applicable.",
    )

    is_default: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether this is the default workflow.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether the workflow is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    company: Mapped["Company"] = relationship(
        back_populates="approval_workflows",
    )

    steps: Mapped[list["ApprovalWorkflowStep"]] = relationship(
        back_populates="workflow",
        cascade="all, delete-orphan",
        order_by="ApprovalWorkflowStep.sequence",
    )