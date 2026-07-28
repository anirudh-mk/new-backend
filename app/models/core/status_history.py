from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.company.company import Company
    from app.models.company.branch import Branch
    from app.models.core.document_type import DocumentType
    from app.models.accounting.journal_status import JournalStatus
    from app.models.user.user import User


class StatusHistory(BaseModel):
    """
    Centralized table storing workflow status transitions for all documents.
    """

    __tablename__ = "status_histories"

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
        doc="Company that owns this status history.",
    )

    branch_id: Mapped[UUID] = mapped_column(
        ForeignKey("branches.id"),
        nullable=False,
        index=True,
        doc="Branch that owns this status history.",
    )

    document_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("document_types.id"),
        nullable=False,
        index=True,
        doc="Type of document.",
    )

    document_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        index=True,
        doc="Primary key UUID of the document.",
    )

    previous_status_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("journal_statuses.id"),
        nullable=True,
        index=True,
        doc="Previous status.",
    )

    current_status_id: Mapped[UUID] = mapped_column(
        ForeignKey("journal_statuses.id"),
        nullable=False,
        index=True,
        doc="Current status.",
    )

    changed_by: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
        doc="User who changed the status.",
    )

    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        doc="Date and time of transition.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Remarks detailing the status transition.",
    )

    # Relationships
    company: Mapped["Company"] = relationship()
    branch: Mapped["Branch"] = relationship()
    document_type: Mapped["DocumentType"] = relationship()
    previous_status: Mapped["JournalStatus"] = relationship(foreign_keys=[previous_status_id])
    current_status: Mapped["JournalStatus"] = relationship(foreign_keys=[current_status_id])
    changed_by_user: Mapped["User"] = relationship(foreign_keys=[changed_by])

    def __repr__(self) -> str:
        return f"<StatusHistory(document_id='{self.document_id}', current_status_id='{self.current_status_id}')>"
