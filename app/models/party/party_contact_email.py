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
    from app.models.party.party_contact import PartyContact


class PartyContactEmail(AuditModel):
    """
    Represents an email address associated with a Party Contact.

    Purpose:
        Stores one or more email addresses for a contact person.
        Each contact may have multiple email addresses for different
        business purposes such as work, personal, billing or support.

    Examples:

        John Mathew

            • john@company.com
            • sales@company.com
            • accounts@company.com

    Business Benefits:
        - Supports multiple email addresses.
        - Allows different email types.
        - Enables email verification.
        - Supports primary email selection.

    Relationships:
        PartyContact
            └── PartyContactEmail
    """

    __tablename__ = "party_contact_emails"

    __table_args__ = (
        UniqueConstraint(
            "contact_id",
            "email",
            name="uq_party_contact_email",
        ),
    )

    contact_id: Mapped[UUID] = mapped_column(
        ForeignKey("party_contacts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Contact that owns this email address.",
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        doc="Email address.",
    )

    email_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="WORK",
        doc="Email type (WORK, PERSONAL, BILLING, SUPPORT, etc.).",
    )

    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        index=True,
        doc="Indicates whether this is the primary email.",
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether this email has been verified.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
        doc="Indicates whether this email is active.",
    )

    # Relationships

    contact: Mapped["PartyContact"] = relationship(
        back_populates="emails",
        lazy="selectin",
        doc="Contact associated with this email.",
    )
