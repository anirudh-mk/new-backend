from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.company.branch import Branch
    from app.models.core.contact_type import ContactType


class BranchContact(AuditModel):
    """
    Represents a contact mechanism (e.g. phone number, email address) associated with a Branch.

    Maps contact classification types to a Branch and defines values, primary indicators, and sorting parameters.

    Purpose:
        - Stores contact mechanisms for communication by branch office.
    """

    __tablename__ = "branch_contacts"

    branch_id: Mapped[UUID] = mapped_column(
        ForeignKey("branches.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="The branch associated with this contact.",
    )

    contact_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("contact_types.id"),
        nullable=False,
        index=True,
        doc="The type of communication method (Phone, Email, etc.).",
    )

    value: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        doc="The actual contact number or address.",
    )

    is_primary: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
        doc="Indicates whether this is the primary contact method for the branch.",
    )

    display_order: Mapped[int] = mapped_column(
        default=1,
        nullable=False,
        doc="Display order sequence number.",
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
        doc="Indicates whether the contact record is active.",
    )

    # Relationships
    branch: Mapped["Branch"] = relationship(
        back_populates="contacts",
    )

    contact_type: Mapped["ContactType"] = relationship()

    def __repr__(self) -> str:
        return f"<BranchContact(id={self.id}, value='{self.value}', is_primary={self.is_primary})>"
