from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.company import Company
    from app.models.branch import Branch
    from app.models.core.document_type import DocumentType
    from app.models.user.user import User


class DocumentComment(BaseModel):
    """
    Centralized table storing user comments and discussions for any document.
    """

    __tablename__ = "document_comments"

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
        doc="Company that owns this comment.",
    )

    branch_id: Mapped[UUID] = mapped_column(
        ForeignKey("branches.id"),
        nullable=False,
        index=True,
        doc="Branch that owns this comment.",
    )

    document_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("document_types.id"),
        nullable=False,
        index=True,
        doc="Type of document this comment belongs to.",
    )

    document_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        index=True,
        doc="Primary key UUID of the target document.",
    )

    comment_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        doc="The text content of the comment.",
    )

    commented_by: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
        doc="User who wrote the comment.",
    )

    commented_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        doc="Timestamp of comment creation.",
    )

    is_private: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        doc="Indicates whether the comment is internal/private to the department.",
    )

    # Relationships
    company: Mapped["Company"] = relationship()
    branch: Mapped["Branch"] = relationship()
    document_type: Mapped["DocumentType"] = relationship()
    commented_by_user: Mapped["User"] = relationship(foreign_keys=[commented_by])

    def __repr__(self) -> str:
        return f"<DocumentComment(document_id='{self.document_id}', commented_by='{self.commented_by}')>"
