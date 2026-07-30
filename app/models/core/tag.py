from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    pass  # decoupled: from app.models.company.company import Company
    pass  # decoupled: from app.models.company.branch import Branch
    from app.models.core.document_type import DocumentType


class DocumentTag(BaseModel):
    """
    Centralized table storing generic classification tags for any document.
    """

    __tablename__ = "document_tags"

    company_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Company that owns this tag record.",
    )

    branch_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Branch that owns this tag record.",
    )

    document_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("document_types.id"),
        nullable=False,
        index=True,
        doc="Type of document this tag is associated with.",
    )

    document_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        index=True,
        doc="Primary key UUID of the target document.",
    )

    tag_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="The label/name of the tag.",
    )

    # Relationships
    document_type: Mapped["DocumentType"] = relationship()

    def __repr__(self) -> str:
        return f"<DocumentTag(document_id='{self.document_id}', tag_name='{self.tag_name}')>"