from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.core.contact_category import ContactCategory
    pass  # decoupled: from app.models.company.company import Company


class ContactType(AuditModel):
    """
    Represents a specific contact mechanism sub-type (e.g. Primary Mobile, Office Phone, General Email).

    Purpose:
        - Defines the actual contact mechanism keys used in addresses or contact lists.
    """

    __tablename__ = "contact_types"

    contact_category_id: Mapped[UUID] = mapped_column(
        ForeignKey("contact_categories.id"),
        nullable=False,
        index=True,
        doc="The parent contact category classification.",
    )

    company_id: Mapped[UUID | None] = mapped_column(
        nullable=True,
        index=True,
        doc="Optional company ownership (for custom company-defined types).",
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="Name of the contact type.",
    )

    code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        doc="Short unique code identifying the type.",
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        doc="Optional description.",
    )

    is_system: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
        doc="Indicates whether this is a default system-defined contact type.",
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
        doc="Indicates whether the contact type is active.",
    )

    # Relationships
    contact_category: Mapped["ContactCategory"] = relationship(
        back_populates="contact_types",
    )


    def __repr__(self) -> str:
        return f"<ContactType(id={self.id}, code='{self.code}', name='{self.name}')>"