from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.party.party import Party
    from app.models.party.party_contact_email import PartyContactEmail
    from app.models.party.party_contact_phone import PartyContactPhone


class PartyContact(AuditModel):
    """
    Represents an individual contact person associated with a Party.

    Purpose:
        Stores information about individuals representing a Party.
        A single Party may have multiple contact persons, each responsible
        for different departments or business functions.

        Contact communication details such as email addresses and phone
        numbers are stored in separate tables, allowing each contact to
        maintain multiple communication methods.

    Examples:
        Party:
            ABC Traders

        Contacts:
            • John Mathew (Sales Manager)
            • Priya Nair (Accounts Manager)
            • Rahul Kumar (Purchase Officer)

    ERP Workflow:

        Party
            │
            ▼
        PartyContact
            ├── PartyContactEmail
            └── PartyContactPhone

    Business Benefits:
        - Supports multiple contacts per Party.
        - Allows department-wise contact management.
        - Supports multiple email addresses and phone numbers.
        - Eliminates duplicate contact information.
        - Centralizes communication records.

    Relationships:
        Party
            └── PartyContact

        PartyContact
            ├── PartyContactEmail
            └── PartyContactPhone
    """

    __tablename__ = "party_contacts"

    __table_args__ = (
        UniqueConstraint(
            "party_id",
            "first_name",
            "last_name",
            name="uq_party_contact_name",
        ),
    )

    party_id: Mapped[UUID] = mapped_column(
        ForeignKey("parties.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Party to which this contact belongs.",
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="First name of the contact person.",
    )

    last_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        doc="Last name of the contact person.",
    )

    designation: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        doc="Job title or designation of the contact person.",
    )

    department: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        doc="Department represented by the contact person.",
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Internal remarks or additional information about the contact.",
    )

    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        index=True,
        doc="Indicates whether this is the primary contact for the Party.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
        doc="Indicates whether this contact is active.",
    )

    # Relationships

    party: Mapped["Party"] = relationship(
        back_populates="contacts",
        lazy="selectin",
        doc="Party associated with this contact.",
    )

    emails: Mapped[list["PartyContactEmail"]] = relationship(
        back_populates="contact",
        cascade="all, delete-orphan",
        lazy="selectin",
        doc="Email addresses associated with this contact.",
    )

    phones: Mapped[list["PartyContactPhone"]] = relationship(
        back_populates="contact",
        cascade="all, delete-orphan",
        lazy="selectin",
        doc="Phone numbers associated with this contact.",
    )