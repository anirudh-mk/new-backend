from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.company.company import Company
    from app.models.core.contact_type import ContactType


class CompanyContact(AuditModel):
    """
    Represents a contact mechanism (e.g., primary phone, general email) for a Company.

    A CompanyContact maps standard contact types (defined in ContactType lookup)
    to a Company and defines values, primary indicators, and sorting parameters.

    Purpose:
        - Stores business communication options (email, phone, website, fax) by company.
        - Labels primary/default contacts for communications and notifications.
    """

    __tablename__ = "company_contacts"

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="The company associated with this contact.",
    )

    contact_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("contact_types.id"),
        nullable=False,
        index=True,
        doc="The type/mechanism of communication (Phone, Email, Fax, etc.).",
    )

    value: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        doc="The actual contact address or number (e.g. info@company.com, +12345678).",
    )

    is_primary: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
        doc="Indicates whether this is the primary contact method.",
    )

    display_order: Mapped[int] = mapped_column(
        default=1,
        nullable=False,
        doc="Sorting display order priority.",
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
        doc="Indicates whether this contact entry is active.",
    )

    # Relationships
    company: Mapped["Company"] = relationship(
        back_populates="contacts",
    )

    contact_type: Mapped["ContactType"] = relationship()

    def __repr__(self) -> str:
        return f"<CompanyContact(id={self.id}, value='{self.value}', is_primary={self.is_primary})>"
