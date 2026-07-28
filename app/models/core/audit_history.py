from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    DateTime,
    ForeignKey,
    JSON,
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


class AuditHistory(BaseModel):
    """
    Centralized table storing field-level changes and actions for audit.
    """

    __tablename__ = "audit_histories"

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
        doc="Company that owns this audit record.",
    )

    branch_id: Mapped[UUID] = mapped_column(
        ForeignKey("branches.id"),
        nullable=False,
        index=True,
        doc="Branch that owns this audit record.",
    )

    document_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("document_types.id"),
        nullable=False,
        index=True,
        doc="Type of document modified.",
    )

    document_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        index=True,
        doc="Primary key UUID of the modified document.",
    )

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="Action performed (e.g. Created, Updated, Approved, Printed).",
    )

    performed_by: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
        doc="User who performed the action.",
    )

    performed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        doc="Timestamp of the action.",
    )

    old_values: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
        doc="JSON snapshot of field values prior to change.",
    )

    new_values: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
        doc="JSON snapshot of new field values after change.",
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True,
        doc="IP address of the client.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional notes regarding changes.",
    )

    # Relationships
    company: Mapped["Company"] = relationship()
    branch: Mapped["Branch"] = relationship()
    document_type: Mapped["DocumentType"] = relationship()
    performed_by_user: Mapped["User"] = relationship(foreign_keys=[performed_by])

    def __repr__(self) -> str:
        return f"<AuditHistory(document_id='{self.document_id}', action='{self.action}')>"
