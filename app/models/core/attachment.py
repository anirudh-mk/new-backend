from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.company.company import Company
    from app.models.company.branch import Branch
    from app.models.core.document_type import DocumentType
    from app.models.user.user import User


class DocumentAttachment(BaseModel):
    """
    Centralized table storing file attachments for any document type in the ERP.
    """

    __tablename__ = "document_attachments"

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
        doc="Company that owns this attachment.",
    )

    branch_id: Mapped[UUID] = mapped_column(
        ForeignKey("branches.id"),
        nullable=False,
        index=True,
        doc="Branch that owns this attachment.",
    )

    document_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("document_types.id"),
        nullable=False,
        index=True,
        doc="Type of document this attachment is linked to.",
    )

    document_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        index=True,
        doc="Primary key UUID of the target document.",
    )

    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        doc="Stored file name.",
    )

    original_file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        doc="Original file name uploaded by the user.",
    )

    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        doc="Storage path of the uploaded file.",
    )

    file_extension: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        doc="File extension (e.g. pdf, jpg, png).",
    )

    mime_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        doc="MIME type of the uploaded file.",
    )

    file_size: Mapped[int] = mapped_column(
        nullable=False,
        doc="File size in bytes.",
    )

    uploaded_by: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
        doc="User who uploaded the attachment.",
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        doc="Date and time when the file was uploaded.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional remarks about the attachment.",
    )

    # Relationships
    company: Mapped["Company"] = relationship()
    branch: Mapped["Branch"] = relationship()
    document_type: Mapped["DocumentType"] = relationship()
    uploaded_by_user: Mapped["User"] = relationship(foreign_keys=[uploaded_by])

    def __repr__(self) -> str:
        return f"<DocumentAttachment(file_name='{self.file_name}', type='{self.file_extension}')>"
