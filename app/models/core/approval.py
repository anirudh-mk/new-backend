from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    pass  # decoupled: from app.models.company.company import Company
    pass  # decoupled: from app.models.company.branch import Branch
    from app.models.core.document_type import DocumentType
    pass  # decoupled: from app.models.user.user import User
    pass  # decoupled: from app.models.accounting.journal_status import JournalStatus
    from app.models.core.approval_history import ApprovalHistory


class Approval(BaseModel):
    """
    Centralized table storing approvals for any document type in the ERP.
    """

    __tablename__ = "approvals"

    company_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Company that owns this approval.",
    )

    branch_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Branch that owns this approval.",
    )

    document_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("document_types.id"),
        nullable=False,
        index=True,
        doc="Type of document being approved.",
    )

    document_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        index=True,
        doc="Primary key UUID of the document being approved.",
    )

    approval_level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
        doc="Approval workflow level/step.",
    )

    approver_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="User responsible for approving.",
    )

    status_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Current approval status.",
    )

    approved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Date and time when the approval was completed.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Approval comments or remarks.",
    )

    # Relationships
    document_type: Mapped["DocumentType"] = relationship()
    
    approval_history: Mapped[list["ApprovalHistory"]] = relationship(
        back_populates="approval",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Approval(document_id='{self.document_id}', level={self.approval_level})>"