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
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.core.approval import Approval
    from app.models.user.user import User
    from app.models.accounting.journal_status import JournalStatus


class ApprovalHistory(BaseModel):
    """
    Centralized table storing workflow history steps for approvals.
    """

    __tablename__ = "approval_histories"

    approval_id: Mapped[UUID] = mapped_column(
        ForeignKey("approvals.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Reference to the Approval header.",
    )

    level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        doc="Approval level at this history step.",
    )

    approver_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
        doc="Approver for this level.",
    )

    status_id: Mapped[UUID] = mapped_column(
        ForeignKey("journal_statuses.id"),
        nullable=False,
        index=True,
        doc="Status set at this level.",
    )

    action_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        doc="Date and time when the approval action was performed.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Approval comments or remarks.",
    )

    # Relationships
    approval: Mapped["Approval"] = relationship(back_populates="approval_history")
    approver: Mapped["User"] = relationship()
    status: Mapped["JournalStatus"] = relationship()

    def __repr__(self) -> str:
        return f"<ApprovalHistory(approval_id='{self.approval_id}', level={self.level})>"
