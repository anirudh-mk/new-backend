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
    pass  # decoupled: from app.models.company.company import Company
    pass  # decoupled: from app.models.company.branch import Branch
    from app.models.core.document_type import DocumentType
    pass  # decoupled: from app.models.accounting.journal_status import JournalStatus
    pass  # decoupled: from app.models.user.user import User


class StatusHistory(BaseModel):
    """
    Centralized table storing workflow status transitions for all documents.
    """

    __tablename__ = "status_histories"

    company_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Company that owns this status history.",
    )

    branch_id: Mapped[UUID] = mapped_column(
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
        nullable=True,
        index=True,
        doc="Previous status.",
    )

    current_status_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Current status.",
    )

    changed_by: Mapped[UUID] = mapped_column(
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
    document_type: Mapped["DocumentType"] = relationship()

    def __repr__(self) -> str:
        return f"<StatusHistory(document_id='{self.document_id}', current_status_id='{self.current_status_id}')>"