from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.core.attachment_type import AttachmentType
    from app.models.party.party import Party


class PartyAttachment(AuditModel):
    """
    Represents a document or file associated with a Party.

    Purpose:
        Stores metadata for files related to a Party. Documents may include
        legal registrations, tax certificates, agreements, identity proofs,
        bank documents, licenses, and other supporting records.

        The actual file should be stored in an external file storage system
        while this table maintains the metadata and reference to the file.

    Examples:

        ABC Traders

            • GST Certificate
            • PAN Card
            • Trade License
            • Bank Passbook
            • Signed Agreement

    ERP Workflow:

        Party
            │
            ▼
        PartyAttachment
            │
            ▼
        File Storage

    Business Benefits:
        - Centralizes all Party-related documents.
        - Supports unlimited attachments.
        - Eliminates duplicate document storage.
        - Simplifies document verification.
        - Reusable across Sales, Purchase, Finance and CRM modules.

    Relationships:
        Party
            └── PartyAttachment

        AttachmentType
            └── PartyAttachment
    """

    __tablename__ = "party_attachments"

    __table_args__ = (
        UniqueConstraint(
            "party_id",
            "attachment_type_id",
            "file_name",
            name="uq_party_attachment",
        ),
    )

    party_id: Mapped[UUID] = mapped_column(
        ForeignKey("parties.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Party that owns this attachment.",
    )

    attachment_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("attachment_types.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        doc="Classification of the attachment.",
    )

    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        doc="Original name of the uploaded file.",
    )

    stored_file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        doc="Unique filename used internally in file storage.",
    )

    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        doc="Storage path or object key of the uploaded file.",
    )

    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="MIME type of the uploaded file (e.g. application/pdf, image/png).",
    )

    file_size: Mapped[int] = mapped_column(
        nullable=False,
        doc="File size in bytes.",
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        doc="Optional description of the attachment.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
        doc="Indicates whether this attachment is active.",
    )

    # Relationships

    party: Mapped["Party"] = relationship(
        back_populates="attachments",
        lazy="selectin",
        doc="Party associated with this attachment.",
    )

    attachment_type: Mapped["AttachmentType"] = relationship(
        back_populates="attachments",
        lazy="selectin",
        doc="Classification assigned to this attachment.",
    )
