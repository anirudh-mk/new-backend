from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.core.contact_type import ContactType


class ContactCategory(AuditModel):
    """
    Represents a high-level grouping/category for contact methods (e.g. Phone, Address, Social).

    Purpose:
        - Classifies different communication channels.
    """

    __tablename__ = "contact_categories"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        doc="Name of the contact category.",
    )

    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        doc="Short unique code for the contact category.",
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        doc="Optional description.",
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
        doc="Indicates whether the category is active.",
    )

    # Relationships
    contact_types: Mapped[list["ContactType"]] = relationship(
        back_populates="contact_category",
        cascade="all, delete-orphan",
        doc="The communication sub-types belonging to this category.",
    )

    def __repr__(self) -> str:
        return f"<ContactCategory(id={self.id}, code='{self.code}', name='{self.name}')>"
