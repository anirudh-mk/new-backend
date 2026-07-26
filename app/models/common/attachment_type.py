from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.party.party_attachment import PartyAttachment


class AttachmentType(AuditModel):
    """
    Represents a configurable classification for Party Attachments.

    Purpose:
        Attachment Types define the business purpose of documents associated
        with a Party. Instead of hardcoding document categories such as
        GST Certificate or Trade License, attachment classifications are
        maintained as configurable master data.

        This allows organizations to introduce new document categories
        without requiring database schema or application changes.

    Examples:
        - GST Certificate
        - PAN Card
        - Trade License
        - Bank Document
        - Agreement
        - Insurance
        - Passport
        - Other

    ERP Workflow:

        Attachment Type
              │
              ▼
        Party Attachment
              │
              ▼
            Party

    Business Benefits:
        - Eliminates hardcoded document types.
        - Supports unlimited attachment categories.
        - Simplifies document organization.
        - Improves reporting and filtering.
        - Reusable across Sales, Purchase, Finance, HR and CRM modules.

    Relationships:
        AttachmentType
            └── PartyAttachment
    """

    __tablename__ = "attachment_types"

    __table_args__ = (
        UniqueConstraint(
            "code",
            name="uq_attachment_type_code",
        ),
        UniqueConstraint(
            "name",
            name="uq_attachment_type_name",
        ),
    )

    code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
        doc=(
            "Unique business code identifying the attachment type. "
            "Examples: GST_CERTIFICATE, PAN_CARD, AGREEMENT."
        ),
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        doc="Display name of the attachment type.",
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        doc="Optional description explaining the purpose of the attachment type.",
    )

    is_system: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc=(
            "Indicates whether this is a system-defined attachment type. "
            "System types are typically protected from deletion."
        ),
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
        doc="Indicates whether this attachment type is active.",
    )

    # Relationships

    attachments: Mapped[list["PartyAttachment"]] = relationship(
        back_populates="attachment_type",
        cascade="all, delete-orphan",
        lazy="selectin",
        doc="Collection of Party Attachments assigned to this attachment type.",
    )
